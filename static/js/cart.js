// Cart Button
var cartBtn = document.getElementsByClassName('update-cart')




for (var i = 0; i < cartBtn.length; i++){
    cartBtn[i].addEventListener('click', function(){

        productId = this.dataset.product
        console.log('user')

        if(user != 'None'){
            updateUserOrder(productId)
            
        }else {
            window.location.replace("/user/login/")
        }
    })
}

function updateUserOrder(productId){
    console.log('User is logged in, sending data...')
    var url = '/shop/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken
        },
        body: JSON.stringify({'productId' : productId})
    })
}


// Cart scroll down

mybutton = document.getElementById("cart_icon")
window.onscroll = function() {scrollFunctionCartIcon()};
function scrollFunctionCartIcon() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
        } else {
        mybutton.style.display = "none";
        }
}

// Update Quantity In Cart Icon

