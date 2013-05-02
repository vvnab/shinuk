function calckAmount(){
  var amount = 0;
  $('table span').each(function(){
    var quantity = $(this).parent().prev().children('input').attr('value');
    amount += parseInt($(this).attr('title')) * quantity;
  });
  return amount;
}

function delElement(){
//  $('')
}


$(document).ready(function(){
  $('input[type="text"]').mask('9');
  $('#amount').html('Всего без учёта доставки на сумму: {0} р.'.format(intcomma(calckAmount())));
  $('input[type="text"]').bind('keyup', function(){
    $('#amount').html('Всего без учёта доставки на сумму: {0} р.'.format(intcomma(calckAmount())));
  });
});