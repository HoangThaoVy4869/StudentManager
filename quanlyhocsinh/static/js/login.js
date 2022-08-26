// Doi tuong
function Validator(options) {

    function getParent(element, selector){
        while (element.parentElement){
            if (element.parentElement.matches(selector)){
                return element.parentElement
            }
            element = element.parentElement
        }
    }

    var selectorRules = {}

    // Ham thuc hien validate
    function validate(inputElement, rule) {
        var errorElement = getParent(inputElement, options.formGroupSelector).querySelector(options.errorSelector);
        var errorMessage

        // Lay ra cac rules cua selector
        var rules = selectorRules[rule.selector]

        // Lap qua tung rule & kiem tra
        // Neu co loi thi dung viec ktra
        for (var i = 0; i < rules.length; ++i) {
            errorMessage = rules[i](inputElement.value)
            if(errorMessage) break
        }

        if (errorMessage){
            errorElement.innerText = errorMessage;
            getParent(inputElement, options.formGroupSelector).classList.add('invalid');
        } else {
            errorElement.innerText = '';
            getParent(inputElement, options.formGroupSelector).classList.remove('invalid');
        }

        return !errorMessage
    }

    // Lay elements cua form validate
    var formElement = document.querySelector(options.form);
    if(formElement){
        formElement.onsubmit = function(e){
            e.preventDefault()

            var isFormValid = true;

            // Lap qua tung rules & validate
            options.rules.forEach(function(rule){
                var inputElement = formElement.querySelector(rule.selector);
                var isValid = validate(inputElement, rule);
                if (!isValid){
                    isFormValid = false;
                }
            })

            if(isFormValid){
                // TH1: Submit voi javascript
                if (typeof options.onSubmit === 'function'){
                    var enabledInput = formElement.querySelectorAll('[name]:not([disabled])')
                    var formValues = Array.from(enabledInput).reduce(function(values, input){
                        (values[input.name] = input.value)
                        return values;
                    }, {})

                    options.onSubmit(formValues)
                }
                // TH2: Submit voi hanh vi mac dinh
                else {
                    formElement.submit();
                }
            }
        }

        // Lap qua moi rule va xu ly (lang nghe skien: blur, input,...)
        options.rules.forEach(function(rule){

            // Luu lai cac rules cho moi input

            if (Array.isArray(selectorRules[rule.selector])){
                selectorRules[rule.selector].push(rule.test);
            }else {
                selectorRules[rule.selector] = [rule.test]
            }

            var inputElement = formElement.querySelector(rule.selector);

            if (inputElement){
                // Xu ly truong hop blur khoi input
                inputElement.onblur = function(){
                    validate(inputElement, rule);
                }

                // Xu ly moi khi nguoi dung nhap vao input
                inputElement.oninput = function(){
                    var errorElement = getParent(inputElement, options.formGroupSelector).querySelector(options.errorSelector);
                    errorElement.innerText = '';
                    getParent(inputElement, options.formGroupSelector).classList.remove('invalid');

                }
            }
        });
    }
}



// Dinh nghia rules
Validator.isRequired = function(selector, message){
    return{
        selector:selector,
        test:function (value){
            return value.trim() ? undefined : message || 'Vui lòng nhập trường này'

        }
    }
}

Validator.isEmail = function(selector, message){
    return{
        selector:selector,
        test:function (value){
            var regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
            return regex.test(value) ? undefined : message || 'Vui lòng nhập đúng email'

        }
    }
}

Validator.minLength = function(selector, min, message){
    return{
        selector:selector,
        test:function (value){
            return value.length >= min ? undefined : message || 'Vui lòng nhập mật khẩu'

        }
    }
}
