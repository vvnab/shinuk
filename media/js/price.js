function en2ru(en){
  var ru = 0;
  if (en < 50) {
    ru = en * 90;
  } else if(en < 100) {
    ru = en * 85;
  } else if(en < 200) {
    ru = en * 80;
  } else {
    ru = en * 75;
  }
  return ru;
}

function ru2en(ru){
  var en = 0;
  if (ru < 4500) {
    en = ru / 90;
  } else if (ru < 8500) {
    en = ru / 85;
  } else if (ru < 16000) {
    en = ru / 80;
  } else {
    en = ru / 75;
  }
  return en;
}