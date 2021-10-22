// function to go back when clicked
function goBack() {
    window.history.back();
}


// function to add or subtract number in number field
$(document).ready(function() {
    $('.minus').click(function() {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 0 ? 0 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function() {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
});

const ordersUls = document.querySelectorAll('.curr-order-lst')

for (let orderUl of ordersUls) {
    orderUl.addEventListener('click', (e) => {
        e.target.classList.toggle('strike')
        console.dir(e.target)
        console.log(`${e.target} got clicked`)
    })
}