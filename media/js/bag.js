function post_to_url(path, params, method) {
  method = method || "post"; 
  var form = document.createElement("form");
  form.setAttribute("method", method);
  form.setAttribute("action", path);

  for(var i in params) {
    for(var key in params[i]) {
      var hiddenField = document.createElement("input");
      hiddenField.setAttribute("type", "hidden");
      hiddenField.setAttribute("name", key);
      hiddenField.setAttribute("value", params[i][key]);

      form.appendChild(hiddenField);
    }
  }

  document.body.appendChild(form);
  form.submit();
}


var wishList = {
  'things': null,
  'count' : 0,
  'pos'   : 0,
  'init'  : function() {
              this.things = $.getCookie('wishList');
              var count = 0;
              var pos = 0;
              for (var i in this.things) {
                count++;
                pos = i;
              };
              this.count = count;
              this.pos = parseInt(pos);
            },
  'add'   : function(thing) {
              var things = this.things;
              for (var i in things) {
                if (parseInt(things[i].art) == thing.art) {
                  if (things[i].color == thing.color) {
                    if (things[i].size == thing.size) {
                      return;
                    }
                  }
                }
              }
              thing.name = '';
              $.setSubCookie('wishList', ++this.pos, thing, {'expires': 30});
              var tst = $.getSubCookie('wishList', this.pos);
              if (!tst) {
                var things = $.getCookie('wishList');
                for (var i in things){
                  break;
                };
                $.removeSubCookie('wishList', i);
                $.setSubCookie('wishList', this.pos, thing, {'expires': 30})
              };
              wishList.init();
            },
  'remove': function(id) {
              $.removeSubCookie('wishList', id);
              var bag = $.getCookie('wishList');
              $.setCookie('wishList', bag, {'expires': 30});
            },
  'clear':  function() {
              $.removeCookie('wishList');
            },
}

var Bag = {
  'things': null,
  'summ'  : 0,
  'count' : 0,
  'pos'   : 0,
  'show'  : false,
  'init'  : function() {
              this.things = $.getCookie('bag');
              var count = 0;
              var summ = 0;
              var pos = 0;
              for (var i in this.things) {
                count++;
                summ += parseInt(this.things[i].price);
                pos = i;
              };
              this.count = count;
              this.summ = summ;
              this.pos = parseInt(pos);
              $('a.bag div').text('{1} р. ({0} шт.)'.format(count, intcomma(summ)));
              this.draw();
            },
  'add'   : function(thing) {
              var things = this.things;
              for (var i in things) {
                if (parseInt(things[i].art) == thing.art) {
                  if (things[i].color == thing.color) {
                    if (things[i].size == thing.size) {
                      return;
                    }
                  }
                }
              }
              $.setSubCookie('bag', ++this.pos, thing, {'expires': 4/24});
              var tst = $.getSubCookie('bag', this.pos);
              if (!tst) {
                var things = $.getCookie('bag');
                for (var i in things){
                  break;
                };
                $.removeSubCookie('bag', i);
                $.setSubCookie('bag', this.pos, thing, {'expires': 4/24})
              };
              Bag.init();
            },
  'remove': function(id) {
              $.removeSubCookie('bag', id);
              var bag = $.getCookie('bag');
              $.setCookie('bag', bag, {'expires': 4/24});
            },
  'clear':  function() {
              $.removeCookie('bag');
            },
  'el'    : function(thing, id) {
              var html = '\
              <a class="thing" href="/shop/model/{5}/">\
              <img alt="" src="{0}"/>\
              <div class="desc">\
              <div class="price">{1} р.</div>\
              <div class="name">{2}</div>\
              <div class="color">{3}</div>\
              <div class="size">{4}</div>\
              </div>\
              <div class="clear"></div>\
              <div class="remove" id="art_{6}"></div>\
              </a>\
              '.format(thing.img, intcomma(thing.price), thing.name, thing.color_ru, thing.size_ru, thing.art, id);
              return html;
            },
  'html'  : function() {
              var html = '';
              for (var i in this.things) {
                html = this.el(this.things[i], i) + html;
              };
              html = '<h4>Ваша корзина заказов:</h4><hr/><div class="scroll2">' + html;
              html += '\
              </div><hr/><a class="bagclear">очистить</a><div class="price2">ВСЕГО: {0} р.</div><hr/>\
              <div class="buybutton"></div><input class="favorites" type="button" value="Заказ / избранное"/>\
              '.format(intcomma(this.summ));
              return html;
            },
  'draw'  : function(){
              if (!this.show){
                $('div#bag').css('visibility', 'hidden');
                $('div#bag').show();
              };
              $('div#bag').html(this.html());
              $('.remove').bind('click', function(){
                var art = $(this).attr('id').split('_')[1];
                Bag.remove(art);
                Bag.init();
                return false;
              });
              $('.bagclear').bind('click', function(){
                Bag.clear();
                Bag.show = false;
                Bag.init();
              });
              $('.scroll2').jScrollPane({contentWidth: 290});
              $('input[type="button"]').button();
              if (!this.show){
                $('div#bag').hide();
                $('div#bag').css('visibility', 'visible');
              };
              $('.buybutton').bind('click', function(){
                var things = new Array();
                for (key in Bag.things) {
                  var quantity = $('.bag input[name="{0}"]'.format(Bag.things[key].art)).attr('value') ? $('.bag input[name="{0}"]'.format(Bag.things[key].art)).attr('value') : 1;
                  things.push({'art': Bag.things[key].art, 'color': Bag.things[key].color, 'size': Bag.things[key].size, 'quantity': quantity, 'price': Bag.things[key].price});
                }
                post_to_url('/order/checkout/', things);
              });
              $('.favorites').bind('click', function(){
                document.location.href = '/bag/';
              });
            }
};

$(document).ready(function(){
  wishList.init();
  Bag.init();
  $('a#abag').bind('mouseenter', function(){
    $(this).oneTime(750, function(){
      $('div#bag').slideDown('slow');
      Bag.show = true;
    });
  });
  $('a#abag').bind('click', function(){
    $(this).stopTime();
  });
  $('a#abag').bind('mouseleave', function(){
    $(this).stopTime();
  });
  $('div#bag').bind('mouseleave', function(){
    $(this).oneTime(750, function(){
      $('div#bag').slideUp('slow');
      Bag.show = false;
    });
  });
  $('div#bag').bind('mouseenter', function(){
    $(this).stopTime();
  });
});
