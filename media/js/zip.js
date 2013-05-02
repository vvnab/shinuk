function getAdds(zip, callback) {
  $.ajax({
    url: 'http://zip.wab-net.ru/zip/' + zip + '/',
    dataType: 'json',
    success: function(adds){alert(adds);}
  });  
}