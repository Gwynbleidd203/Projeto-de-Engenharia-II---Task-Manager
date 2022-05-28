function deleteAnimation() {
    document.getElementById("icon-delete").setAttribute("src", "{{ url_for('static', filename='icons/delete-filled.svg')}}")
}