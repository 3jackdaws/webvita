let Sidepanel = {
    Basics: {
        load: function () {
            Resume.getObjectsOfType('basics', function(objects){
                let $panel = $('#sidepanel-basics');
                $panel.html('');
                $.each(objects, function (i, e) {
                    console.log(e);
                    let div = $(`<div class="rs-item rs-sidepanel-item basic" data-name="${e.data.tag}">${e.data.value}</div>`);
                    div[0].meta = e;
                    $panel.append(div);
                });
                Sidepanel.makeDraggable();
            });
        },
        showModal:function (event) {
            event.preventDefault();
            event.stopPropagation();
            var content = `
            <form class='ui form' id="modal-form">
                <div class="field">
                    <label>Tag Name</label>
                    <input name="tag" placeholder="cellphone">
                </div>
                <div class="field">
                    <label>Value</label>
                    <input name="value" placeholder="(555)555-5555">
                </div>
            </form>
    
            `;

            var buttons = `
                <button class='ui negative button'>CANCEL</button>
                <button class='ui positive button' onclick='Resume.createObject("basics", Form2Object($("#modal-form")), Sidepanel.Basics.load)'>ADD</button>
            `;
            Modal.display('Enter Basic Info', content, buttons);
        }
    },
    Education:{
        load:function () {
            Resume.getObjectsOfType('education', function(objects){
                let $panel = $('#sidepanel-education');
                $panel.html('');
                $.each(objects, function (i, e) {
                    let edu = $(`<div class="rs-item rs-sidepanel-item education">${ e.data.school }<br><b>${ e.data.degree }</b></div>`);
                    edu[0].meta = e;
                    $panel.append(edu);
                });
                Sidepanel.makeDraggable();
            });
        },
        showModal:function (event) {
            event.preventDefault();
            event.stopPropagation();
            var content = `
            <form class='ui form' id="modal-form">
                <div class="field">
                    <label>School</label>
                    <input name="school" placeholder="">
                </div>
                <div class="field">
                    <label>Degree or Certification</label>
                    <input name="degree" placeholder="">
                </div>
                <div class="field">
                    <label>Date</label>
                    <input name="date" placeholder="">
                </div>
            </form>
    
            `;

            var buttons = `
                <button class='ui negative button'>CANCEL</button>
                <button class='ui positive button' onclick='Resume.createObject("education", Form2Object($("#modal-form")), Sidepanel.Education.load)'>ADD</button>
            `;
            Modal.display('Enter Education', content, buttons);
        }
    },
    Experience:{
        load:function () {
            Resume.getObjectsOfType('experience', function(objects){
                let $panel = $('#sidepanel-experience');
                $panel.html('');
                $.each(objects, function (i, e) {
                    let edu = $(`<div class="rs-item rs-sidepanel-item experience">${ e.data.title }</div>`);
                    edu[0].meta = e.data;
                    $panel.append(edu);
                });
                Sidepanel.makeDraggable();
            });
        },
        showModal:function (event) {
            event.preventDefault();
            event.stopPropagation();
            var content = `
            <form class='ui form' id="modal-form">
                <div class="field">
                    <label>Title</label>
                    <input name="title" placeholder="Senior Project">
                </div>
                <div class="field">
                    <label>Short Description</label>
                    <textarea name="description"></textarea>
                </div>
                <div class="field">
                    <label>Date</label>
                    <input name="date" placeholder="">
                </div>
            </form>
    
            `;

            var buttons = `
                <button class='ui negative button'>CANCEL</button>
                <button class='ui positive button' onclick='Resume.createObject("experience", Form2Object($("#modal-form")), Sidepanel.Experience.load)'>ADD</button>
            `;
            Modal.display('Enter Experience', content, buttons);
        }
    },
    Skills:{
        load:function () {
            let objectType = 'skills';
            Resume.getObjectsOfType(objectType, function(objects){
                let $panel = $('#sidepanel-' + objectType);
                $panel.html('');
                $.each(objects, function (i, e) {
                    let div = $(`<div class="rs-item rs-sidepanel-item skill">${ e.data.skill }</div>`);
                    div[0].meta = e;
                    $panel.append(div);
                });
                Sidepanel.makeDraggable();
            });
        },
        showModal:function (event) {
            event.preventDefault();
            event.stopPropagation();
            var content = `
            <form class='ui form' id="modal-form">
                <div class="field">
                    <label>Name</label>
                    <input name="skill" placeholder="Technical Writing">
                </div>
            </form>
    
            `;

            var buttons = `
                <button class='ui negative button'>CANCEL</button>
                <button class='ui positive button' onclick='Resume.createObject("skills", Form2Object($("#modal-form")), Sidepanel.Skills.load)'>ADD</button>
            `;
            Modal.display('Add Skill', content, buttons);
        }
    },
    Layouts:{
        load:function () {
            let objectType = 'layout';
            Resume.getObjectsOfType(objectType, function(objects){
                let $panel = $('#sidepanel-' + objectType + 's');
                $panel.html('');
                $.each(objects, function (i, e) {
                    let active = '';
                    if (e.id === CurrentResume.layout) {
                        active = 'active';
                    }
                    let div = $(`<div class="rs-sidepanel-item item layout ${active}" onclick="Sidepanel.Layouts.select(${e.id})">Layout ${ e.id }</div>`);
                    div[0].meta = e;
                    $panel.append(div);
                });
                Sidepanel.makeDraggable();

            });
        },
        select:function(id){
            Resume.getObject(id, function (layout) {
                console.log(layout);
                $('#resume').html(layout.data.text);
                CurrentResume.layout = id;
                MakeResumeDraggable();
                Sidepanel.Layouts.load();
            })
        },
        showModal:function (event) {
            event.preventDefault();
            event.stopPropagation();
            var content = `
            <form class='ui form' id="modal-form">
                <div class="field">
                    <label>Layout Markup</label>
                    <textarea name="text"></textarea>
                </div>
            </form>
    
            `;

            var buttons = `
                <button class='ui negative button'>CANCEL</button>
                <button class='ui positive button' onclick='Resume.createObject("layout", Form2Object($("#modal-form")), Sidepanel.Layouts.load)'>ADD</button>
            `;
            Modal.display('Add Layout', content, buttons);
        }
    },
    Themes:{
        load:function () {
            let objectType = 'theme';
            Resume.getObjectsOfType(objectType, function(objects){
                let $panel = $('#sidepanel-' + objectType + 's');
                $panel.html('');
                $.each(objects, function (i, e) {
                    let active = '';
                    if (e.id === CurrentResume.theme) {
                        active = 'active';
                    }
                    let div = $(`<div class="rs-sidepanel-item item ${objectType} ${active}" onclick="Sidepanel.Themes.select(${e.id})">Theme ${ e.id }</div>`);
                    div[0].meta = e;
                    $panel.append(div);
                });
                Sidepanel.makeDraggable();
            });
        },
        select:function(id){
            Resume.getObject(id, function (theme) {
                console.log(theme);
                $('#styles').html(theme.data.text);
                CurrentResume.theme = id;
                Sidepanel.Themes.load();
            })
        },
        showModal:function (event) {
            event.preventDefault();
            event.stopPropagation();
            var content = `
            <form class='ui form' id="modal-form">
                <div class="field">
                    <label>Theme Markup</label>
                    <textarea name="text"></textarea>
                </div>
            </form>
    
            `;

            var buttons = `
                <button class='ui negative button'>CANCEL</button>
                <button class='ui positive button' onclick='Resume.createObject("theme", Form2Object($("#modal-form")), Sidepanel.Themes.load)'>ADD</button>
            `;
            Modal.display('Add Theme', content, buttons);
        }
    },
    Scripts:{},
    makeDraggable:function () {
        $.each($('.rs-sidepanel'), function (i, e) {
            Sortable.create(e, {
                group: {name: "rs", pull: 'clone', put:false},
                ghostClass:'item-ghost',
                sort:true,
                onClone:function (event) {
                    event.clone.meta = event.item.meta;
                }
            });
        });
    },
    refreshAll:function () {
        Sidepanel.Basics.load();
        Sidepanel.Education.load();
        Sidepanel.Experience.load();
        Sidepanel.Skills.load();
        Sidepanel.Layouts.load();
        Sidepanel.Themes.load();
    }
};