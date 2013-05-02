Array.prototype.max = function(){
    return Math.max.apply( Math, this );
};

Array.prototype.min = function(){
    return Math.min.apply( Math, this );
};

$(document).ready(function(){
  $('span.helptext').hide();

  $('#fetch').bind('click', fetch);
  if (urlModel) {
    $('input[name="href"]').attr('value', urlModel);
    fetch();
  }

  $('#id_group').bind('change', function(){
    var group = $('#id_group :selected').attr('value');
    $.ajax({
      url: '/ladmin/get_categorys/',
      type: 'GET',
      dataType: 'json',
      data: {group: group},
      beforeSend: function(){
        showLoader();
      },
      success: function(resp){
        var categorys = resp.categorys;
        $('#id_category').empty();
        for (var i in categorys){
          $('#id_category').append('<option value="{0}">{1}</option>'.format(categorys[i].id, categorys[i].name));
        }
      },
      error: function(){
        alert('Произошла ошибка!');
      },
      complete: function(){
        hideLoader();
      }
    });
  });
});

function setSize(obj, cl){
  var val =$(obj).attr('value');
  $(cl).attr('value', val);
}

function fetch(){
  var url = $('input[name="href"]').attr('value');
  $.ajax({
    url: '/ladmin/model_fetch/',
    type: 'GET',
    dataType: 'json',
    data: {url: url},
    beforeSend: function(){
      showLoader();
    },
    success: function(resp){
      fetchResult(resp.url, resp.created, resp.categorys, resp.colors, resp.baseColors, resp.selcats);
    },
    error: function(){
      alert('Произошла ошибка!');
    },
    complete: function(){
      hideLoader();
      $('a').fancybox({'autoScale': false});
    }
  });
};

function fetchResult(obj, created, categorys, colors, baseColors, selcats){
//Добавление новых полей в списки
  if (created.group) {
    $('#id_group').append('<option value="{0}">{1}</option>'.format(created.group.id, created.group.name));
  }
  if (created.brand) {
    $('#id_brand').append('<option value="{0}">{1}</option>'.format(created.brand.id, created.brand.name));
  }

//Выбор опций
  $('#id_vendor :contains("'+obj.vendor+'")').attr("selected", "selected");
  $('#id_brand :contains("'+obj.brand+'")').attr("selected", "selected");
//  $('#id_group :contains("'+obj.group+'")').attr("selected", "selected");
  $('#id_group option').each(function(i, o){
    if ($(this).text() == obj.group) $(this).attr("selected", "selected");
  });
  if (obj.group){
    $('#id_category').empty();
    for (var i in categorys[obj.group]){
      $('#id_category').append('<option value="{0}">{1}</option>'.format(categorys[obj.group][i].id, categorys[obj.group][i].name));
    }
  }
  if (obj.subcategory) {
    var category = obj.category + ' → ' + obj.subcategory;
    $('#id_category :contains("'+category+'")').attr("selected", "selected");
  } else {
    var category = obj.category;
    $('#id_category :contains("'+category+'")').attr("selected", "selected");
    $('#id_category :contains("'+category+' → ")').attr("selected", "");
  }
  for (var i=0;i<selcats.length;i++) {
    $('#id_category [value={0}]'.format(selcats[i])).attr("selected", "selected");
  }
  
//
  var html = '';
  var htmlInfo = '';
  htmlInfo += '<div><i>{0}</i> : <i>{1}</i> : <i>{2}</i> : <b><i>{3}</i></b></div>'.format(obj.group, obj.category, obj.subcategory, obj.brand);
  $('#id_name').attr('value', obj.name);
  htmlInfo += '<div><b>{0}</b></div>'.format(obj.name);
  $('#id_art').attr('value', obj.art);
  $('#id_url').attr('value', obj.url);
  $('#id_flashurl').attr('value', obj.flashurl);
  $('#id_description').attr('value', obj.description);
  $('#id_info').attr('value', obj.info);
  $('.img_all').empty();
  for (var i = 0; i < obj.images.all.length; i++) {
      $('.img_all').append('<a target="_blank" href="{0}"><img src="{1}"/></a>'.format(obj.images.all[i].lage, obj.images.all[i].small, obj.images.all[i].lage));
      $('.img_all').append('<input type="hidden" name="images_all" value="{0}"/>'.format(obj.images.all[i].small));
      $('.img_all').append('<input type="hidden" name="images_all" value="{0}"/>'.format(obj.images.all[i].thumb));
      $('.img_all').append('<input type="hidden" name="images_all" value="{0}"/>'.format(obj.images.all[i].medium));
      $('.img_all').append('<input type="hidden" name="images_all" value="{0}"/>'.format(obj.images.all[i].lage));
  }

  for (var i in obj.items) {
    html += '<input type="hidden" name="colors" value="{0}">'.format(i);
    html += '<h4 style="float: left">{0}</h4>'.format(i);
    html += '<div style="margin-left: 150px" class="size">';
    html += '<input type="text" value="{0}" name="color_{1}"/> цвет<br/>'.format(colors[i].name_ru, i);
    html += '<input type="text" value="{0}" name="color_{1}" class="baseColor"/> базовый цвет<br/>'.format(colors[i].base, i);
    html += '<input type="text" value="{0}" name="color_{1}" class="rgbColor" /> код цвета <div class="colorBox" style="background-color: #{0}"></div><br/>'.format(colors[i].rgb, i);
    html += '</div><hr/>';
    if (obj.images[i]) {
      html += '<a target="_blank" style="display: block; float: left; margin-right: 20px" href="{0}"><img alt="" src="{1}"/></a>'.format(obj.images[i].lage, obj.images[i].small);
      html += '<input type="hidden" name="images_{0}" value="{1}"/>'.format(i, obj.images[i].small);
      html += '<input type="hidden" name="images_{0}" value="{1}"/>'.format(i, obj.images[i].thumb);
      html += '<input type="hidden" name="images_{0}" value="{1}"/>'.format(i, obj.images[i].medium);
      html += '<input type="hidden" name="images_{0}" value="{1}"/>'.format(i, obj.images[i].lage);
    }
    html += '<ol>';
    var price = [0];
    var oldprice = [0];
    for (var c=0;c < obj.items[i].length;c++){
      if (obj.items[i][c].present){ 
        html += '<div class="size"><li><input onKeyUp="setSize(this, \'.size_{4}\')" class="size_{4}" name="size_{4}_{5}" type="text" value="{6}"/> {1} <sub>[{0}]</sub> : {2}&pound; : <small>{7}&pound;</small></li></div>'.format(obj.items[i][c].size, obj.items[i][c].size_en, obj.items[i][c].price, obj.items[i][c].present, obj.items[i][c].size, i, obj.items[i][c].size_ru, obj.items[i][c].oldprice);
        html += '<input type="hidden" name="sizes_{0}" value="{1}"/>'.format(i, obj.items[i][c].size);
        price.push(obj.items[i][c].price);
        oldprice.push(obj.items[i][c].oldprice);
      }
    }
    html += '</ol><div class="clear"></div><hr class="strong"/>';
    html += '<input type="hidden" name="price_{0}" value="{1}"/>'.format(i, price.max());
    html += '<input type="hidden" name="price_{0}" value="{1}"/>'.format(i, oldprice.max());
  }
  html += '<input type="submit" value="сохранить"/>';

  $('.response').html(html);
  $('.baseInfo').html(htmlInfo);
  $('.baseInfo').show();
  $('.baseColor').autocomplete({
    source: baseColors
  });
  $('.rgbColor').bind('keyup', function(){
    var rgb = $(this).attr('value');
    $(this).next().css('background-color', '#'+rgb);
  });
}
