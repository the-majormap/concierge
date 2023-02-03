import axios from './core/client.js';

class MainList {
    constructor(listObj, chiceObj, procs) {
        this.proc = {...procs};
        this.listObj = listObj;
        this.choiceObj = chiceObj;
        this.limit = 20;
        console.log(this);
    }

    numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    rangePicker = (obj, max) => {
        let numberWithCommas = this.numberWithCommas
        var $range = obj;
        var $picker = obj.find("div.ic-range-picker");

        var $upperPicker = obj.find('div.upper-picker');
        var $valueRange = obj.find('div.value-range');
        var $upperValue = obj.find('input.upper-value');


        var leftOffset = $range.offset().left;
        var rangeWidth = $range.width();
        var leftOffall = leftOffset + rangeWidth;


        var setLowerPickerValue = function (value) {

            var width = $upperPicker.offset().left;
            $valueRange.css({
                left: `${value}px`,
                width: `${width}px`,
            });
            var translatedValue = Math.floor(value / rangeWidth * max);

        };
        $upperPicker.click(function (e) {
            e.stopImmediatePropagation();
        })

        $range.click(function (e) {
            setUpperPickerValue(e.offsetX)
        })

        var setUpperPickerValue = function (value) {
            $upperPicker.css({
                left: `${value}px`,
            });

            var width = rangeWidth - (leftOffall - $upperPicker.offset().left) + 4;
            $valueRange.css({
                width: `${width}px`,
            });
            var translatedValue = Math.floor(value / rangeWidth * max);
            $upperValue.val(numberWithCommas(translatedValue));
            $upperValue.css({
                left: `${value}px`,
            });
        };
        $upperValue.blur(function (e) {
            var $this = $(this);
            var value = $this.val().replace(',', '') / max * rangeWidth;
            setUpperPickerValue(value);
        });

        $upperValue.keydown(function (key) {
            if (key.keyCode === 13) {
                var $this = $(this);
                var value = $this.val() / max * rangeWidth;
                setUpperPickerValue(value);
            }
        });

        $picker.mousedown(function (e) {
            var $this = $(this);
            e = e || window.event;
            e.preventDefault();
            var elem = $this;
            var left = $this.offset().left - ($this.width() / 2);

            document.onmouseup = function () {
                document.onmouseup = null;
                document.onmousemove = null;
            };

            var min = leftOffset;
            var max = min + $range.width();


            document.onmousemove = function (e) {
                e = e || window.event;
                e.preventDefault();


                var left = e.clientX - $range.offset().left;
                if (e.clientX < min) {
                    left = min - $range.offset().left;
                } else if (e.clientX > max) {
                    left = max - $range.offset().left;
                }

                if (elem.hasClass('lower-picker')) {
                    setLowerPickerValue(left);
                } else if (elem.hasClass('upper-picker')) {
                    setUpperPickerValue(left);
                }
            };
        });
        setUpperPickerValue($upperValue.val() / max * rangeWidth);
    }

    listCall(payload) {
        console.log(this.proc.method);
        if (typeof this.proc.method !== "undefined" && this.proc.method == "post") {
            return axios.post(this.proc.src, payload);
        } else {
            return axios.get(this.proc.src, payload);
        }
    }

    addChoic = (el) => {
        el.currentTarget.classList.add("on")
        let listObj = this.listObj;
        let choiceObj = this.choiceObj;
        let rangePicker = this.rangePicker;
        let $ = this.proc.$;

        const obj_name = this.proc.obj_name
        let clone = el.currentTarget.cloneNode(true);
        clone.id = "chice_" + obj_name + "_" + clone.dataset.id;
        clone.insertAdjacentHTML("beforeend", `<div class="multi-range" >            
            <div class="value-range" ></div>
            <div class="ic-range-picker upper-picker"></div>         
            <input class="input value upper-value" type="text" value="100"  />
        </div>`)


        let close_btn = document.createElement("button");
        close_btn.classList.add("close");
        close_btn.insertAdjacentHTML("beforeend", `<i class="icon-edc-ic-close"></i>`)
        close_btn.addEventListener("click", function (ell) {
            listObj.querySelector(`#Item_${obj_name}_${ell.currentTarget.parentNode.dataset.id}`).classList.remove("on");
            ell.currentTarget.parentNode.remove();
        });
        clone.insertAdjacentElement("beforeend", close_btn);
        choiceObj.insertAdjacentElement("beforeend", clone);


        let multi_range = $(`#${clone.id} .multi-range`);
        rangePicker(multi_range, 100);
    }


    listMake = async () => {
        let lists = await this.listCall({});
        let listObj = this.listObj.querySelector(".swiper-wrapper");

        let name = typeof this.proc.name == "undefined" ? "name" : this.proc.name;
        let id = typeof this.proc.id == "undefined" ? "id" : this.proc.id;
        listObj.innerHTML = "";
        let limit = this.limit;
        let paging_limit = 0;
        let paging_obj, item_obj;
        let addChoic = this.addChoic;
        let $ = this.proc.$;
        const obj_name = this.proc.obj_name

        lists.forEach(function (obj, key) {
            if (key >= paging_limit) {
                paging_obj = document.createElement("div");
                paging_obj.className = "paging_wrap swiper-slide"
                listObj.insertAdjacentElement("beforeend", paging_obj);
                paging_limit = paging_limit + limit;
            }
            item_obj = document.createElement("div");
            item_obj.dataset.id = obj[id];
            item_obj.id = "Item_" + obj_name + "_" + obj[id];


            item_obj.insertAdjacentHTML("beforeend", `<span class="text">${obj[name]}</span>`);
            item_obj.addEventListener("click", addChoic);
            paging_obj.insertAdjacentElement("beforeend", item_obj);
        });

        var swiper = new Swiper(this.listObj, {
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });
        return false;
    }
}

(() => {

    let $keyword_list = new MainList(document.querySelector(".keyword_list"), document.querySelector(".keyword_choice_list"), {
        $: $,
        src: "/api/keyword/list?id=324",
        name: "keyword",
        obj_name: "keyword"
    });
    $keyword_list.listMake();


    let $search_list = new MainList(document.querySelector(".subject_list"), document.querySelector(".subject_choice_list"), {
        $: $,
        src: "/api/subjects/list",
        method: "post",
        obj_name: "search"
    });
    $search_list.listMake();

    let sumitbtn = document.querySelector(".submit_button");
    sumitbtn.addEventListener("click", function () {
        var arr = [];
        let keyword_choice_list_div = document.querySelectorAll(".keyword_choice_list > div");
        let subject_choice_list_div = document.querySelectorAll(".subject_choice_list > div");

        function arrinput(ob, tp) {
            ob.forEach(function (obj) {
                arr.push({"type": tp, "id": obj.dataset.id, "score": obj.querySelector("input.value").value})
            });
        };
        arrinput(document.querySelectorAll(".keyword_choice_list > div"), "word")
        arrinput(document.querySelectorAll(".subject_choice_list > div"), "subject")

        console.log(arr);
        axios.post("/api/filters/input", arr);


    });

})()
