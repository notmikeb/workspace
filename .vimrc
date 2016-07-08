" Vundle
set nocompatible             " not compatible with the old-fashion vi mode
filetype off                 " required!

" http://www.erikzaadi.com/2012/03/19/auto-installing-vundle-from-your-vimrc/
" Setting up Vundle - the vim plugin bundler
let iCanHazVundle=1
let vundle_readme=expand('~/.vim/bundle/vundle/README.md')
if !filereadable(vundle_readme)
	echo "Installing Vundle.."
	echo ""
	silent !mkdir -p ~/.vim/bundle
	silent !git clone https://github.com/gmarik/vundle ~/.vim/bundle/vundle
	let iCanHazVundle=0
endif

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required!
Bundle 'gmarik/vundle'

" Plugin
Bundle 'scrooloose/syntastic'
Bundle 'majutsushi/tagbar'
Bundle 'godlygeek/tabular'
Bundle 'float-tw/easyreST'

" Plugin settting

" Syntastic
let g:syntastic_auto_loc_list=1

" tagbar
let g:tagbar_left=1

set ruler
set number
set showmode
set shiftwidth=4
set tabstop=4
set backspace=2
set incsearch
set hls
set nocompatible
set showcmd
set autoindent
set cindent
set cursorline
set title
"set colorcolumn=80
set guifontset=8x16,kc15f,-*-16-*-big5-0 
"set fenc=big5 enc=big5 tenc=utf8
"set fenc=gb2312 enc=gb2312 tenc=utf8
set foldmethod=indent
set foldlevel=10
"autocmd BufEnter * call DoWordComplete()
syntax on
set t_Co=256
colorscheme desert
"colorscheme evening
"colorscheme default
"set background=light
"set background=dark

highlight Comment ctermfg=darkcyan
highlight Search term=reverse ctermbg=4 ctermfg=7

" encodings
set fileencodings=ucs-bom,utf-8,big5,gbk
set termencoding=utf-8
set encoding=utf-8

" map
nmap <F12> <esc>:Tagbar<CR><C-w>h
imap <F12> <esc>:Tagbar<CR><C-w>h
nmap <F9> <esc>:set list!<CR>
imap <F9> <esc>:set list!<CR>
nmap <F10> <esc>:set paste!<CR>
nmap <F5> <esc>:set linebreak!<CR>
imap <F5> <esc>:set linebreak!<CR>
set pastetoggle=<F10>
nmap <F7> gT
nmap <F8> gt

" set K use man first then sdcv
:set keywordprg=bash\ -c\ \'man\ $0\ \|\|\ sdcv\ $0\'

" status line
set laststatus=2 "ls=2
set statusline=%<%F "file name
set statusline+=\ [%{&fileencoding},%{&fileformat}]
set statusline+=\ %1*%m%* "modified
set statusline+=%= "
set statusline+=%h%r\ %-19([%p%%]%4b\ 0x%-4B\ %3l,%02c%03V%)%y
"highlight StatusLine term=bold,reverse cterm=bold,reverse
highlight User1 term=reverse cterm=reverse ctermbg=darkred


" persistent undo
set undofile
set undodir=~/.vim/undodir
set undolevels=1000

" wil
set wildmode=longest:full
set wildmenu

" filetype
filetype on
filetype indent on
filetype plugin on

" list
set nolist
set listchars=tab:>-,trail:-

" tab indent
imap <S-Tab> <C-o><<
vmap <Tab> >
vmap <S-Tab> <

" spell check
map <F2> :set spell!<CR><Bar>:echo "Spell check: " . strpart("OffOn", 3 * &spell, 3)<CR>
imap <F2> <esc>:set spell!<CR><Bar>:echo "Spell check: " . strpart("OffOn", 3 * &spell, 3)<CR>
hi clear SpellBad
hi SpellBad term=underline cterm=underline ctermfg=red

" auto write python coding info
function PyHeader()
	if getfsize(@%) <= 0
		execute "norm i#!/usr/bin/env python\n# -*- coding: utf-8 -*-"
	endif
endfunction

au BufRead,BufNewFile *.py call PyHeader()

" automatically removing all trailing whitespace
function TrailingWhitespace()
	if search('\s\+$', 'wn') != 0
		execute '%s/\s\+$//e'
		execute "norm ''"
	endif
endfunction

autocmd FileType c,cpp,python autocmd BufWritePre <buffer> call TrailingWhitespace()

" less mode
function! LessMode()
	if g:lessmode == 0
		let g:lessmode = 1
		let onoff = 'on'
		" Scroll half a page down
		noremap <script> d <C-D>
		" Scroll one line down
		noremap <script> j <C-E>
		" Scroll half a page up
		noremap <script> u <C-U>
		" Scroll one line up
		noremap <script> k <C-Y>
	else
		let g:lessmode = 0
		let onoff = 'off'
		unmap d
		unmap j
		unmap u
		unmap k
	endif
	echohl Label | echo "Less mode" onoff | echohl None
endfunction
let g:lessmode = 0
nnoremap <F4> :call LessMode()<CR>
inoremap <F4> <Esc>:call LessMode()<CR>


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" cscope setting
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if has("cscope")
  set csprg=/usr/bin/cscope
  set csto=1
  set cst
  set nocsverb
  " add any database in current directory
  if filereadable("cscope.out")
  cs add cscope.out
  endif
  set csverb
endif
"
nmap <C-e>s :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <C-e>g :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <C-e>c :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <C-e>t :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap <C-e>e :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap <C-e>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <C-e>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <C-e>d :cs find d <C-R>=expand("<cword>")<CR><CR>
