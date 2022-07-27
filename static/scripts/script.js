/* Set the width of the side navigation to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

/* MODAL FORM */

function openForm() {
document.getElementById("create-form").style.display = 'block'
}

function closeForm() {
document.getElementById("create-form").style.display = 'none'
}

/* MODAL LOGIN */

function openLogin() {
document.getElementById("login-form").style.display = 'block'
}

function closeLogin() {
document.getElementById("login-form").style.display = 'none'
}

/* MODAL CREATE ACCOUNT */

function openCreateAccount () {
  document.getElementById("create-account").style.display = 'block'
}

function closeCreateAccount () {
  document.getElementById("create-account").style.display = 'none'
}

/* MODAL CREATE TYPE */

function openCreateTipo () {
  document.getElementById("create-tipo").style.display = 'block'
}

function closeCreateTipo () {
  document.getElementById("create-tipo").style.display = 'none'
}

/* MODAL FILTERS */

function closeFilter () {
  document.getElementById("filter").style.display = 'none'
}

function openFilter () {
  document.getElementById("filter").style.display = 'block'
}

/* AJAX */

function showNewTask() {
  let xhr = new XMLHttpRequest()
  
  xhr.open("GET", "{{url_for('lista_de_tarefas')}}", true)
  xhr.send()
}