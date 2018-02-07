/**
 * Created by imurphy on 7/24/17.
 */




function Form2Object(form){
    var data = $(form).serializeArray();
    var obj = {};
    
    $.each(data, function (i, param) {
        obj[param.name] = param.value;
    });
    return obj;
}

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }



function AjaxSendForm(event, callback){
    event.preventDefault();
    var form = event.target;
    var url = form.action;
    var data = null;
    if(form.method.toUpperCase() === 'GET'){
        var getParameters = $(form).serialize();
        url += '?' + getParameters;
    }else if(form.method.toUpperCase() === 'POST'){
        data = Form2Object(form);
    }

    $.ajax({
        url:url,
        method:form.method,
        data:data,
        complete:function(xhr){
            if(callback)callback(xhr.responseText, xhr.status);
        }
    })
}

var Message = {
    getHTML:function(title, content, klass){
        return `
            <div class="ui message ${klass}">
                <div class="header">
                    ${title}
                </div>
                <p>${content}</p>
            </div>
        `;
    }
};


function LogoutUser(){
    $.ajax({
        url:'/api/sessions',
        method:'DELETE',
        success:function () {
            window.location = '/';
        }
    })
}


var Resume = {
    resumeEndpoint:'/api/resumes/',
    createNewResume:function (name, callback) {
        $.post({
            url:Resume.resumeEndpoint,
            data:{
                name:name
            },
            method:'POST',
            success:callback
        })
    },
    fetchResume:function(id, callback){
        $.ajax({
            url:Resume.resumeEndpoint + id + '/',
            method:'GET',
            success:callback
        })
    },
    saveResume:function(id, markup, callback){
        $.ajax({
            url:Resume.resumeEndpoint + id + '/',
            method:'PUT',
            data:{layout:markup},
            success:callback
        })
    }
};