$(document).ready(function(){
    $(document).on('click','.add-to-cart-button',function(){
        var _vm = $(this);
        var _index = _vm.attr('data-index');
        var _qty = $('.product-quantity-'+_index).val();
        var _productId = $('.product-id-'+_index).val();
        var _productImage = $('.product-image-'+_index).val();
        var _productName = $('.product-name-'+_index).val();
        var _productPrice = $('.product-price-'+_index).text();
        var text = _vm.text();
        

        $.ajax({
            url:'/add-to-cart',
			data:{
                'id':_productId,
                'productImage':_productImage,
                'qty':_qty,
                'productName':_productName,
                'productPrice':_productPrice,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
                
                
			},
			success:function(res){
                $(".cart-quantity").text(res.totalItems);
                
                _vm.attr('disabled',false);
                
			}
        });
    });
    $(document).on('click','.delete-item',function(){
        var _vm = $(this);
        var _pId = $(this).attr('data-item');
        $.ajax({
            url:'/delete-from-cart',
			data:{
                'id':_pId,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
                $(".cart-quantity").text(res.totalItems);
                _vm.attr('disabled',false);
                $("#cart-list").html(res.data)
			}
        });
    });

    $(document).on('click','.update-item',function(){
        var _vm = $(this);
        var _pId = $(this).attr('data-item');
        var _pQty = $(".product-quantity-"+_pId).val();
        $.ajax({
            url:'/update-cart',
			data:{
                'id':_pId,
                'qty':_pQty,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
                // $(".cart-quantity").text(res.totalItems);
                _vm.attr('disabled',false);
                $("#cart-list").html(res.data)
			}
        });
    });

    // Activate Selected Address
    $(document).on('click','.activate-address',function(){
        var _vm = $(this);
        var _aId = $(this).attr('data-address');
        $.ajax({
            url:'/activate-address',
			data:{
                'id':_aId,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
                if(res.bool==true){
                    $(".address").removeClass('shadow border-secondary');
                    $(".address"+_aId).addClass('shadow border-secondary');

                    $(".check").hide();
                    $(".actbtn").show();

                    $(".check"+_aId).show();
                    $(".btn"+_aId).hide();
                }
			}
        });
    });


});