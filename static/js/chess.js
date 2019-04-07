$(document).ready(function (evt) {

    let selection = {
        ctrl: function (el) {
            $(el).toggleClass(this.cl);
        },
        cl: "selected",
        selBtn: function () {
            let btns = $("#buttons");
            let sel = $(".selected");
            let btnsBool = btns.hasClass("d-none");
            let selBool = sel.length === 0;
            if (selBool) {
                if (!btnsBool) {
                    btns.addClass("d-none");
                }
            } else if (!selBool && btnsBool) {
                btns.removeClass("d-none");
            }
        }
    };

    let dragObj = {};

    $(".date").on({
        // dblclick: function (e) {
        //     $(this).toggleClass('selected');
        // },
        mousedown: function (e) {
            if (!$(this).hasClass('sel-test')) {
                if (e.button === 0) {
                    selection['ctrl'](this);
                    $(".date").on('mouseenter', function () {
                        $(this).toggleClass('selected');
                    });
                }
            }

            let elem = e.target.closest('.sel-test');
            if (!elem) return;

            dragObj.elem = elem;
            dragObj.downX = e.pageX;
            dragObj.downY = e.pageY;
        },
        mouseup: function (e) {
            $(".date").off('mouseenter');
            if (e.button === 0) {
                selection.selBtn();
            }
        }
    });

    $("#cancel").click(function () {
        $(".date").removeClass("selected");
        $("#buttons").addClass("d-none");
        $(".sel-move").css("position", "unset");
    });
    $("#accept").click(function () {
        let obj = new Object();

        let sel = $(".selected");
        for (let i = 0; i < sel.length; i++) {
            let typeRoom = sel.eq(i).parent().parent().children(".block-header").children(".type-room")[0].innerText;
            let room = sel.eq(i).parent().children(".room")[0].innerText;
            let day = sel[i].innerText;
            if (obj[typeRoom]) {
                if (obj[typeRoom][room]) {
                    obj[typeRoom][room].push(day);
                } else {
                    obj[typeRoom][room] = [];
                    obj[typeRoom][room].push(day);
                }
            } else {
                obj[typeRoom] = {};
                obj[typeRoom][room] = [];
                obj[typeRoom][room].push(day);
            }
        }
        console.log(obj);

        dataPerson(obj);

    });

    $('.sel-test').draggable({

        containment: '.testing',

        drag: function (event, ui) {
            // $(this).css({'background': 'red'});
            $(this).css({
                'position': 'relative',
            })
        },
        revert: true

    });
    $('.date').droppable({

        drop: function (event, ui) {

            $(this).droppable({disabled: true});
            // $(ui.draggable).draggable({revert: false, disabled: true}).addClass("selected");
            $(ui.draggable).draggable({revert: false, disabled: true}).addClass("sel-move");
            $(ui.draggable).position({
                at: 'center',
                my: 'center',
                of: this
            });

            selection.selBtn();
        }

    });

//    Сверка даты со страницы
    let day = function (day) {
        return {
            1: 'Пн',
            2: 'Вт',
            3: 'Ср',
            4: 'Чт',
            5: 'Пт',
            6: 'Сб',
            0: 'Вс'
        }[day]
    };

    let now = new Date();
    let nowDay = day(now.getDay()) + ' ' + now.getDate();

    let weekday = $(".weekday");
    for (let i=0; i<weekday.length; i++) {
        if (weekday[i].innerText === nowDay) {
            $(weekday[i]).addClass('now-line');
        }
    }

});