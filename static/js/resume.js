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
    saveResume:function(id, data, callback){
        $.ajax({
            url:Resume.resumeEndpoint + id + '/',
            method:'PUT',
            data:data,
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
    update:function(id, data, callback){
        $.ajax({
            url:Resume.resumeEndpoint + id + '/',
            method:'PUT',
            data:data,
            success:callback
        })
    },
    getObject:function(id, callback){
        $.ajax({
            url:'/api/objects/' + id,
            method:'GET',
            success:function (results) {
                try{
                    results.data = JSON.parse(results.data);
                }catch(e){

                }
                callback(results);
            }
        })
    },
    createObject:function (type, data, callback) {
        if(typeof data === 'object' || typeof data === 'array'){
            data = JSON.stringify(data);
        }
        $.ajax({
            url:'/api/objects/',
            method:'POST',
            data:{
                type:type,
                data:data
            },
            success:function (results) {
                try{
                    results.data = JSON.parse(results.data);
                }catch(e){

                }
                callback(results);
            }
        })
    },
    deleteObject:function(id, callback){
        $.ajax({
            url:'/api/objects/'+ id,
            method:'DELETE',
            success:callback
        });
    },
    getObjectsOfType:function (type, callback) {
        $.ajax({
            url:'/api/objects/?type=' + type,
            method:'GET',
            success:function (results) {
                console.log(results);
                let decodedResults = [];
                $.each(results, function (i,e) {
                    try{
                        e.data = JSON.parse(e.data);
                    }catch(x){

                    }
                    decodedResults.push(e);
                });

                callback(decodedResults);
            }
        })
    }

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