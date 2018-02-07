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
    },

};

let User = {
    fetchAttributes:function(callback){
        $.ajax({
            url:'/api/attributes',
            method:'GET',
            success:callback
        })
    }
};