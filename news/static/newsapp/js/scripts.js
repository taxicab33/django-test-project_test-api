// Получение переменной cookie по имени
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Настройка AJAX
$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function like(){
    var like = $(this);
    var type = like.data('type');
    var id = like.data('id');
    var action = like.data('action');
    var dislike = like.next();

    $.ajax({
        url : action,
        method : 'POST',
        data : { 'id' : id,
                 'type': type,
                 'vote_type': action},

        success : function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            if (json.auth_error != null) alert(json.auth_error)
        },
        error: function(json) {
           alert(json.result)
        }
    });

    return false;
}

function dislike(){
    var dislike = $(this);
    var type = dislike.data('type');
    var id = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url : action,
        method : 'POST',
        data : { 'id' : id,
                 'type': type,
                 'vote_type': action},
        success : function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
            if (json.auth_error != null) alert(json.auth_error)
        },
        error: function(json) {
           alert(json.auth_error)
        }
    });

    return false;
}

function auth_error(json){
    if (json.auth_error != null) alert(json.auth_error)
}

function convert_to_month_name(time){
    return String(time.toLocaleString('ru', { month: 'long' }));
}

function get_only_time(datetime){
    hours = datetime.getHours();
    if (Number(hours) < 10) hours = "0" + hours;
    minutes = datetime.getMinutes();
    if (Number(minutes) < 10) minutes = "0" + minutes;
    time = String(hours + ":" + minutes + " ")
    return time;
}

function convert_time(raw_datetime){
    var datetime = new Date(Date.parse(raw_datetime));
    time = get_only_time(datetime);
    month = convert_to_month_name(datetime).slice(0,3);
    month = month[0].toUpperCase() + month.slice(1,3)
    date = datetime.getDate()
    if (Number(date) < 10){
        date =  "0" + date;
    }
    year = datetime.getFullYear()
     return String(date + " " + month + " " + year + " в " + time + " ");
}

function get_time(comment){
    time_create = convert_time(comment.fields.time_create);
    time_update = "";
    if(comment.fields.time_update != comment.fields.time_create){
        time_update = " (изменено в " + convert_time(comment.fields.time_update) + " )"
    }
    return time_create + time_update;
}

function create_comment_menu_btn(parent, action){
    var btn = document.createElement("li");
    var btn_href = document.createElement("a");
    btn_href.setAttribute("class", "dropdown-item " + action + "_comment");
    btn_href.setAttribute("data-action", action + "_comment");
    if(action == "delete") btn_href.innerText = "Удалить";
    if(action == "edit") btn_href.innerText = "Редактировать";
    if(action == "report") btn_href.innerText = "Пожаловаться";
    btn.appendChild(btn_href);
    parent.appendChild(btn);
}

function create_vote_btn(action, comment_pk){
    var li = document.createElement("li");
    li.setAttribute("data-id", comment_pk);
    li.setAttribute("data-type", "Comment");
    li.setAttribute("data-action", action);

    var icon = document.createElement("span");
    if(action == "like"){
        icon.setAttribute("class", "fa-regular fa-thumbs-up");
        li.setAttribute("title", "Нравится");
    }
    else{
        icon.setAttribute("class", "fa-regular fa-thumbs-down");
        li.setAttribute("title", "Не нравится");
    }

    var count_action = document.createElement("span");
    count_action.setAttribute("data-count", action);
    count_action.innerText = " 0 ";

    li.appendChild(icon);
    li.appendChild(count_action);

    return li;
}

function create_vote_div(parent, comment_pk){
    var votes = document.createElement("ul");
    votes.setAttribute("class", "votes");
    votes.appendChild(create_vote_btn("like", comment_pk));
    votes.appendChild(create_vote_btn("dislike", comment_pk));

    parent.appendChild(votes);
}

function update_comments_count(json){
    document.getElementById('comments_count').innerHTML = json.comments_count + ' комментарий';
    auth_error(json);
}

function show_edit_answer_form(){
    var comment;
    var action = $(this).data('action');
    if(action == "edit_comment"){
        comment = $(this).closest('.dropdown-menu');
    }
    else comment = $(this);
    var comment_id = comment.data('comment_id');
    var comment_form = document.getElementById("comment-form-" + comment_id);
    comment_form.classList.remove("d-none");
    var form_btn = comment_form.querySelector('.btn');
    var textarea = comment_form.querySelector(".form-control");
    if (action == "edit_comment"){
        var comment_text = document.getElementById('comment-text-'+comment_id).innerText;
        var textarea = comment_form.querySelector(".form-control");
        form_btn.innerText = "Сохранить";
        comment_form.setAttribute('class',"mb-3 edit-comment-form");
        textarea.innerText = comment_text
    }
    else{
        textarea.innerText = ''
        form_btn.innerText = "Ответить";
        comment_form.setAttribute('class',"mb-3 answer-comment-form");
    }
}

function create_answer_edit_form(parent, comment){
    var form = document.createElement("form");
    form.setAttribute("id", "comment-form-" + comment.pk);
    form.setAttribute("data-comment_id", comment.pk);
    form.setAttribute("data-obj_id", comment.fields.object_id);
    form.classList.add("d-none");

    var input_group = document.createElement("div");
    input_group.setAttribute("class", "input-group");

    var textarea = document.createElement("textarea");
    textarea.setAttribute("class", "form-control");
    textarea.setAttribute("placeholder", "Введите комментарий");
    textarea.setAttribute("rows", "3");
    textarea.innerText = comment.fields.text;
    input_group.appendChild(textarea);
	
    var btn_group = document.createElement("div");
    btn_group.setAttribute("class", "column");
    
    var submit_btn = document.createElement("button");
    submit_btn.setAttribute("class", "btn btn-secondary mt-2");
    submit_btn.setAttribute("type", "submit");
    submit_btn.innerText = "Сохранить";

    var cancel_btn = document.createElement("button");
    cancel_btn.setAttribute("class", "btn btn-secondary mt-2");
    cancel_btn.setAttribute("type", "button");
    cancel_btn.setAttribute("data-action", "cancel_form");
    cancel_btn.innerText = "Отмена";

    form.appendChild(input_group);
    btn_group.appendChild(submit_btn);
    btn_group.appendChild(cancel_btn);
    form.appendChild(btn_group);
    parent.appendChild(form);
}

function get_comment_parent(comment_pk, comment_parent_pk){
    var parent = null;
    if(comment_parent_pk != null){
        parent = document.getElementById('comment-'+comment_parent_pk);
        parent = parent.querySelectorAll('.comment-answer')[0];
    }
    else {
        parent = document.getElementById("comments");
    }
    return parent;
}

function add_comment_html(json){
    update_comments_count(json);
    var comment = JSON.parse(json.comment.replace('[','').replace(']', ''));
    var parent = get_comment_parent(comment.pk, comment.fields.parent)
    var new_comment = document.createElement("div");
    new_comment.setAttribute("class", "user-comment mb-3");
    new_comment.setAttribute("id", "comment-" + comment.pk);

    var user_info = document.createElement("div");
    user_info.setAttribute("class", "user-info");

    var avatar = document.createElement("div");
    avatar.setAttribute("class", "avatar");
    var user_img_href = document.createElement("a");
    user_img_href.setAttribute("href", json.author_url);
    var user_img = document.createElement("img");
    user_img.setAttribute("class", "small-user-image");
    if(json.author_img != null){
        user_img.setAttribute("src", json.author_img);
    }
    else{
        user_img.setAttribute("src", 'static/newsapp/image/no-profile-photo.png');
    }
    user_img_href.appendChild(user_img);
    avatar.appendChild(user_img_href);
    user_info.appendChild(avatar);

    var login = document.createElement("div");
    login.setAttribute("class", "login");
    var author_name = document.createElement("a");
    author_name.setAttribute("href", json.author_url)
    author_name.textContent = json.author_username;
    login.appendChild(author_name);
    user_info.appendChild(login);

    var datetime = document.createElement("div");
    datetime.setAttribute("class", "datetime");
    var small = document.createElement("small");
    small.setAttribute("class", "small");
    small.textContent = get_time(comment);
    datetime.appendChild(small);
    user_info.appendChild(datetime);

    var comment_menu = document.createElement("div");
    comment_menu.setAttribute("class", "btn-group comment_menu");
    var dropdown_btn = document.createElement("button")
    dropdown_btn.setAttribute("class","dropdown-toggle");
    dropdown_btn.setAttribute("type","button");
    dropdown_btn.setAttribute("data-bs-toggle","dropdown");
    dropdown_btn.setAttribute("aria-expanded","false");
    comment_menu.appendChild(dropdown_btn);

    var ul = document.createElement("ul");
    ul.setAttribute("class", "dropdown-menu");
    ul.setAttribute("data-type", "Comment");
    ul.setAttribute("data-comment_id", comment.pk);
    ul.setAttribute("data-object_id", comment.fields.object_id);
    ul.setAttribute("data-user", comment.fields.user);

    create_comment_menu_btn(ul, "edit");
    create_comment_menu_btn(ul, "delete");
    create_comment_menu_btn(ul, "report");
    comment_menu.appendChild(ul);
    user_info.appendChild(comment_menu);
    new_comment.appendChild(user_info);

    var comment_info = document.createElement("div");
    comment_info.setAttribute("class", "comment mt-2");
    var comment_text = document.createElement("p");
    comment_text.setAttribute("id", 'comment-text-'+comment.pk);
    comment_text.innerText = comment.fields.text;
    comment_info.appendChild(comment_text);

    var comment_reactions = document.createElement("div");
    comment_reactions.setAttribute("class", "comment-reactions");
    if(comment.fields.parent == null){
    var answer_btn = document.createElement("p");
    answer_btn.setAttribute("class", "answer-btn");
    answer_btn.setAttribute("data-type", "Comment");
    answer_btn.setAttribute("data-comment_id", comment.pk);
    answer_btn.setAttribute("data-obj_id", comment.fields.object_id);
    answer_btn.setAttribute("data-action", "answer_comment");
    answer_btn.innerText = "Ответить";
    comment_reactions.appendChild(answer_btn);
    }
    create_vote_div(comment_reactions, comment.pk);
    comment_info.appendChild(comment_reactions);

    create_answer_edit_form(comment_info, comment);

    if(comment.fields.parent == null){
        var comment_answer = document.createElement('div');
        comment_answer.setAttribute('class', 'comment-answer');
        comment_info.appendChild(comment_answer);
    }

    new_comment.appendChild(comment_info);
    parent.insertBefore(new_comment, parent.firstChild);
}

function delete_comment_html(json){
    update_comments_count(json);
    if(json.auth_error == null){
        var comment_on_delete = document.getElementById("comment-" + json.comment_id);
        comment_on_delete.parentNode.removeChild(comment_on_delete);
    }
}

function edit_comment_html(json){
    var comment = JSON.parse(json.comment.replace('[','').replace(']', ''));
    var comment_html = document.getElementById('comment-'+comment.pk);
    document.getElementById("comment-form-"+comment.pk).classList.add("d-none");
    comment_html.querySelector('.datetime .small').innerText = get_time(comment);
    document.getElementById('comment-text-'+comment.pk).innerText = comment.fields.text;
}

function type(value) {
  var regex = /^\[object (\S+?)\]$/;
  var matches = Object.prototype.toString.call(value).match(regex) || [];

  return (matches[1] || 'undefined').toLowerCase();
}

function getParent(elemSelector, parentSelector) {
  var elem = document.querySelector(elemSelector);
  var parents = document.querySelectorAll(parentSelector);

  for (var i = 0; i < parents.length; i++) {
    var parent = parents[i];

    if (parent.contains(elem)) {
      return parent;
    }
  }

  return null;
}

function cancel_form(){
    var form = $(this).closest("form");
    var comment_id = form.data('comment_id');
    var comment_form = document.getElementById("comment-form-" + comment_id);
    comment_form.setAttribute('class', 'd-none comment-form-'+comment_id);
}

function add_comment(){
    var form = $(this);
    var comment_id = null
    if (form.data('comment_id') != null){
        comment_id = form.data('comment_id')
        form.addClass('d-none');
    }
    var comment_text = form.find('.form-control').val();
    form.find('.form-control').val('');
    var obj_id = form.data('obj_id');

    if(comment_text.length != 0){
        $.ajax({
            url : 'comment',
            method : 'POST',
            data : {'obj_id': obj_id,
                    'type': 'Article',
                    'action': 'comment',
                    'comment_text': comment_text,
                    'comment_id' : comment_id},
            success : function(json){
            add_comment_html(json);
            },
            error: function(json){
            alert("Ошибка сервера");
            }
        });
    }
    else{
        alert("Напишите комментарий перед отправкой")
    };
    return false;
}

function edit_comment(){
    try{
        var comment_form = $(this);
        var comment_text = comment_form.find('.form-control').val();
        var comment_id = comment_form.data('comment_id');
        var obj_id = comment_form.data('obj_id');
        if(comment_text.length != 0){
            $.ajax({
                url : 'edit_comment',
                method : 'POST',
                data : { 'comment_id': comment_id,
                         'obj_id' : obj_id,
                         'type' : "Article",
                         'action': 'edit_comment',
                         'comment_text': comment_text},
                success : function(json){
                    edit_comment_html(json);
                },
                error: function(json){
                    alert("Ошибка сервера");
                }
            });
    }
    else{
        alert("Напишите комментарий перед отправкой")
    };

    return false;
}
    catch (err){
        alert(err);
        return false;
    }
    }

function delete_comment(){
    var comment = $(this).closest('.dropdown-menu');
    var article_id = comment.data('object_id');
    var comment_id = comment.data('comment_id');

    $.ajax({
    url : 'delete_comment',
    method : 'POST',
    data : { 'obj_id' : article_id,
             'type': 'Article',
             'comment_id': comment_id,
             'action': 'delete_comment'},
    success : function(json){
        delete_comment_html(json)
    },
    error: function(json){
        alert("Ошибка сервера")
    }
    });
    return false;
}

function update_favorite_btn(json, obj){
    if(json.result == true){
        obj.text("Убрать из избранного")
    }
    else{
        obj.text("Добавить в избранное")
    }
}

function favorite(){
    var obj = $(this)

     $.ajax({
    url : 'favorite',
    method : 'POST',
    data : { 'id' : obj.data('id'),
             'type': obj.data('type')},
    success : function(json){
        update_favorite_btn(json, obj)
    },
    error: function(json){
        return false
    }
    });
    return false;
}

// Подключение обработчиков
$(function() {
    $('body').on('click', '[data-action="like"]', like);
    $('body').on('click', '[data-action="dislike"]', dislike);
    $('#comment_form').submit(add_comment);
    $('body').on('submit', '.edit-comment-form', edit_comment);
    $('body').on('submit', '.answer-comment-form', add_comment);
    $('body').on('click', '[data-action="edit_comment"]', show_edit_answer_form);
    $('body').on('click', '.answer-btn', show_edit_answer_form);
    $('body').on('click', '[data-action="favorite"]', favorite);
    $('body').on('click', '[data-action="delete_comment"]', delete_comment);
    $('body').on('click', '[data-action="cancel_form"]', cancel_form);
});