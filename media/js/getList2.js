var sPageSize = 6;
var sPage = 0;
var sCount = 0;
var sPageMax = 0;
var getListLock = false;

function getList(page, category){
    $.ajax({
      url: '/shop/get_goods2/',
      type: 'GET',                                      
      dataType: 'json',
      data: {'page': page, 'page_size': sPageSize, 'category': category},
      beforeSend: function(){
        getListLock = true;
        showLoader('#list2');
      },
      success: function(resp){
        sCount = resp.count;
        sPageMax = Math.ceil(sCount / sPageSize);
        resp = resp.items;
        $('#list2').empty();
        if(resp.length == 0) location.href = location.pathname +'?page=0';
        $('.sInfo').html('{0} - {1} из {2}'.format(sPage * sPageSize + 1, sPage * sPageSize + resp.length, sCount));
        for (var i = 0; i < resp.length; i++){
          var cl = '';
          var clear = '';
          if((i % 2) == 0){
            cl = 'alpha';
          }            
          if((i % 2) == 1){
            cl = 'omega';
            clear = '<div class="clear"></div>';
          }            
          var oldprice = resp[i].oldprice;
          if (oldprice > 0) {
            oldprice = '<div class="oldprice">{0} р.</div>'.format(intcomma(oldprice));
          } else {
            oldprice = '';
          }
          $('#list2').append('<div class="grid_3 {3}"><div class="list_item2"><a class="thing_href" href="/shop/model/{5}/?page={6}"><img src="{0}"/></a><a class="name" href="/shop/model/{5}/?page={6}">{1}</a>{7}<div class="price">{2} р.</div></div></div>{4}'.format(resp[i].imgs[0], resp[i].name, intcomma(resp[i].price), cl, clear, resp[i].art, sPage, oldprice));
        }
      },
      error: function(){
//        alert('Произошла ошибка!');
        getListLock = false;
      },
      complete: function(){
        hideLoader('#list2');
        getListLock = false;
      }
  });
}