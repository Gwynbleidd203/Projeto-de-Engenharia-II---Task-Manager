$(document).ready(function() {
    
    $('.btn').click(function() {
        $.ajax({
            url: '',
            type: 'GET',
            contentType: 'application/json',
            data: {
                button_text: $(this).text()
            },
            sucess: function(response) {
                $('.btn').text(response.seconds)
            }
        })
    })
})


$(document).ready(function() {

    $('#form-task').on('submit', function(event) {
        
        $.ajax({
            data: {
                nome : $('#nome'),
                descricao : $('#descricao'),
                tipo_id : $('#tipo'),
                status_id : $('#status'),
                proridade_id : $('#prioridade'),
                usuario_id : $('#usuario_id'),
                data_prevista : $('#data_prevista')
            },
            type: 'POST',
            url: '/criar'
        })

        event.preventDefault()

    })
})