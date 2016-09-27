

#include <linux/kernel.h>
#include <linux/errno.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/wait.h>
#include <linux/tty.h>
#include <linux/tty_driver.h>
#include <linux/tty_flip.h>
#include <linux/serial.h>
#include <linux/sched.h>
#include <linux/version.h>
#include <asm/uaccess.h>

#include <linux/delay.h>

#define DRIVER_VERSION "v1.2"
#define DRIVER_AUTHOR "Luis Claudio Gamboa Lopes <lcgamboa@yahoo.com>"
#define DRIVER_DESC "mytty null modem driver"

/* Module information */
MODULE_AUTHOR( DRIVER_AUTHOR );
MODULE_DESCRIPTION( DRIVER_DESC );
MODULE_LICENSE("GPL");

//module_param(pairs, short, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);
//MODULE_PARM_DESC(pairs, "Number of pairs of devices to be created, maximum of 128");


#define TTYDRV_MAJOR	31 	/* experimental range */

/* fake UART values */
//out
#define MCR_DTR		0x01
#define MCR_RTS		0x02
#define MCR_LOOP	0x04
//in
#define MSR_CTS		0x10
#define MSR_CD		0x20
#define MSR_DSR		0x40
#define MSR_RI		0x80

#define SCULL_DEBUG 1
        
#if 0
static struct tty_port *tport;

struct mytty_serial {
	struct tty_struct	*tty;		/* pointer to the tty for this device */
	int			open_count;	/* number of times this port has been opened */
	struct semaphore	sem;		/* locks this structure */

	/* for tiocmget and tiocmset functions */
	int			msr;		/* MSR shadow */
	int			mcr;		/* MCR shadow */

	/* for ioctl fun */
	struct serial_struct	serial;
	wait_queue_head_t	wait;
	struct async_icount	icount;
       
};

static struct mytty_serial **mytty_table;	/* initially all NULL */
#endif

// new structure
static struct tty_driver *ttydrv = 0;
struct tty_struct *mytty =0;
static struct tty_port tport;

struct timer_list mytty_timer;
char mybuffer[128];

static int callback(void)
{
pr_info("%s callback data:%d\n", __FUNCTION__, mytty_timer.data);
if( mytty && mytty->port && mytty_timer.data > 0){
tty_insert_flip_string(mytty->port, mybuffer, mytty_timer.data);
tty_flip_buffer_push(mytty->port);
}
return 0;
}

static int mytty_open(struct tty_struct *tty, struct file *file)
{
printk(KERN_DEBUG "%s - \n", __FUNCTION__);
tport.tty = tty;
tty->port = &tport;
pr_info("tty 0x%x port 0x%x\n", tport.tty, tty->port);

mytty = tty;
return 0;
}

static void mytty_close(struct tty_struct *tty, struct file *file)
{
	
#ifdef SCULL_DEBUG
        printk(KERN_DEBUG "%s - \n", __FUNCTION__);
#endif
}	

static int mytty_write(struct tty_struct *tty, const unsigned char *buffer, int count)
{
int retval = count;
int min = 0;
pr_info("%s write count:%d\n", __FUNCTION__, count);
// put to our read buffer
if( count > sizeof(mybuffer)){
	min = sizeof(mybuffer);
}else{
	min = count;
}
memcpy(mybuffer, buffer, min);

#if 1
// wait around 5 second to launch the callback 
// todo: NO semaphone 
mytty_timer.function = callback;
mytty_timer.data = min;
mytty_timer.expires = jiffies + 500;
add_timer(&mytty_timer);
#else
// warning cannot invoke the tty_insert_xxx inside write. it cause dump
tty_insert_flip_string(tty->port, mybuffer, min);
tty_flip_buffer_push(tty->port);
#endif


retval = min;
msleep(20*min);


pr_info("%s exit\n", __FUNCTION__);
return retval;
}

static int mytty_write_room(struct tty_struct *tty) 
{
	int room = -EINVAL;
	room = 255;
	return room;
}

#define RELEVANT_IFLAG(iflag) ((iflag) & (IGNBRK|BRKINT|IGNPAR|PARMRK|INPCK))

static void mytty_set_termios(struct tty_struct *tty, struct ktermios *old_termios)
{
	unsigned int cflag;
	unsigned int iflag;
	
        printk(KERN_DEBUG "%s - \n", __FUNCTION__);

}

static int mytty_ioctl(struct tty_struct *tty,
                      unsigned int cmd, unsigned long arg)
{
	printk(KERN_DEBUG "%s - %04X %x %x %x\n", __FUNCTION__,cmd, TIOCGSERIAL, TIOCMIWAIT, TIOCGICOUNT);

/*
	switch (cmd) {
	case TIOCGSERIAL:
		return mytty_ioctl_tiocgserial(tty, cmd, arg);
	case TIOCMIWAIT:
		return mytty_ioctl_tiocmiwait(tty, cmd, arg);
	case TIOCGICOUNT:
		return mytty_ioctl_tiocgicount(tty, cmd, arg);
	}
*/

	return -ENOIOCTLCMD;
}

static struct tty_operations serial_ops = {
	.open = mytty_open,
	.close = mytty_close,
	.write = mytty_write,
	.write_room = mytty_write_room,
//	.set_termios = mytty_set_termios,
//	.tiocmget = mytty_tiocmget,
//	.tiocmset = mytty_tiocmset,
//	.ioctl = mytty_ioctl,
};


static int __init mytty_init(void)
{
	int retval;
	printk(KERN_INFO DRIVER_DESC " " DRIVER_VERSION "\n");

	ttydrv = alloc_tty_driver(1);
	if(!ttydrv)
		return -ENOMEM;
	ttydrv->owner = THIS_MODULE;
	ttydrv->driver_name = "myttydriver";
	ttydrv->name = "mytty";
	ttydrv->major = TTYDRV_MAJOR;
	ttydrv->type = TTY_DRIVER_TYPE_SERIAL;
	ttydrv->subtype = SERIAL_TYPE_NORMAL;
	ttydrv->flags = TTY_DRIVER_RESET_TERMIOS | TTY_DRIVER_REAL_RAW;

        ttydrv->init_termios = tty_std_termios;
	ttydrv->init_termios.c_iflag = 0;
	ttydrv->init_termios.c_oflag = 0;
	ttydrv->init_termios.c_cflag = B38400|CS8|CREAD;
	ttydrv->init_termios.c_lflag = 0;
	ttydrv->init_termios.c_ispeed = 38400;
	ttydrv->init_termios.c_ospeed = 38400;

	tty_set_operations(ttydrv, &serial_ops);

	memset(&tport, 0 , sizeof(tport));
        tty_port_init(&tport);
	tty_port_link_device(&tport, ttydrv, 0);

	retval = tty_register_driver(ttydrv);

	init_timer(&mytty_timer);
	
	if( retval){
		pr_err("failed to register %d\n", retval);
		put_tty_driver(ttydrv);
	}else{
		retval = 0;
	}
	return retval;
}

static void __exit mytty_exit(void)
{
	struct mytty_serial *mytty;
	int i;
	tty_port_destroy(&tport);
	tty_unregister_device(ttydrv, 0);
	tty_unregister_driver(ttydrv);
	kfree(ttydrv);
	ttydrv = 0;
	
        printk(KERN_DEBUG "%s - \n", __FUNCTION__);

}

module_init(mytty_init);
module_exit(mytty_exit);
