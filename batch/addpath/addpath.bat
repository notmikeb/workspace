@echo off

echo "remove c:\kkk from path env"
set path=%path:c:\kkk;=%

echo "remove duplicated ;; to ; "
set path=%path:;;=;%

echo "add c:\kkk to path env"
set path=%path%;c:\kkk;
