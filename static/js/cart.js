<script>

  $( document ).ready(function() {
    $('.cart-form').submit(function(e){
      e.preventDefault()

      const acc_id = $(this).attr('id')
      console.log(acc_id)
      
      const btnText = $(`.cart-btn${acc_id}`).text()
      const trim = $.trim(btnText)
      console.log(btnText)

      const cart_count = $('#cart1').text()
      const trimCount = parseInt(cart_count)
      console.log(trimCount + 1)

      const url = $(this).attr('action')

      $.ajax({
        type: 'POST',
        url: url,
        data: {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'acc_id':acc_id
        },

        success: function(response) {
          if(trim === 'Remove from Pocket'){
            $(`.cart-btn${acc_id}`).text('Add to Pocket')
            res = trimCount - 1
          } else {
            $(`.cart-btn${acc_id}`).text('Remove from Pocket')
            res = trimCount + 1
            
          }
          const cart_count = $('#cart1').text(res)
        },
        error: function(response){
          console.log("error", response)
        }

      })

   
    })
  })

</script>