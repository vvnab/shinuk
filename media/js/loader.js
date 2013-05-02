function showLoader(div){
  if (!div) var div = '.grid_20';
  $(div).fadeTo('fast', 0.2);
  var offset = $(div).offset();
  var height = $(div).height();
  var width = $(div).width();
  var wheight = $(window).height() - offset.top;
  var scroll = $(document).scrollTop();
//  alert ('height:={0}\nwidth:={1}\nwheight:={2}\nscroll:={3}\ntop:={4}'.format(height, width, wheight, scroll, offset.top))
  if (wheight < height) height = wheight;
  $('body').append('<div id="loader"><img src="/media/loader2.gif"/></div>');
  $('#loader').css('top', offset.top + height/2 - 32 - scroll);
  $('#loader').css('left', offset.left + width/2 - 32);
}

function hideLoader(div){
  if (!div) var div = '.grid_20';
  $(div).fadeTo('fast', 1);
  $('#loader').remove();
}
