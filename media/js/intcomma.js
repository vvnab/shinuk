  function strrevert(s){
    s2 = '';
    for (x = s.length; x >= 0; x--){
        s2 += s.substr(x,1);
    }
    return s2;
  }

  function intcomma(x){
    y = '' + Math.round(x);
    y = strrevert(y);
    r = y.replace(/\d{3}/gi, '$& ');
    return strrevert(r);
  }
