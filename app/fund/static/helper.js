function clear_class(btns, class_name) {
    for (const btn of btns) {
        btn.classList.remove(class_name)
    }
}

function add_class(btns, class_name) {
    for (const btn of btns) {
        btn.classList.add(class_name)
    }
}

function btns_event_listener(btns, obj, key, hide_btns = null) {
    for (const btn of btns) {
        btn.addEventListener('click', (event) => {
            obj[key] = event.target.attributes['id'].value;
            clear_class(btns, "selected-donate-option");
            event.target.classList.add("selected-donate-option")
            console.log(obj)
            if (hide_btns) {
                if (obj[key] == 0 && hide_btns) {
                    add_class(hide_btns, "hide");
                } else {
                    clear_class(hide_btns, "hide");
                }
            }
        })
    }
}

function getVars(vars) {
    return vars
}