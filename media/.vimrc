set fileencodings=utf8
set nocompatible

set nu
set incsearch
set guioptions-=T
set expandtab
set tabstop=2
set autoindent
set nobk
set aw
syntax on
colors darkblue

function InsertTabWrapper()     
    let col = col('.') - 1     
    if !col || getline('.')[col - 1] !~ '\k'         
        return "\<tab>"     
    else         
        return "\<c-p>"     
        endif
endfunction
imap <tab> <c-r>=InsertTabWrapper()<cr>
set complete=""
set complete+=.
set complete+=k
set complete+=b
set complete+=t
set foldmethod=indent
set foldlevel=4
