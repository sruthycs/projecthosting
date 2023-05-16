function inputValidation(inputTxt){

    var regx = /^[0-9a-zA-Z ]+$/;
    var textField = document.getElementById("textField");

    if(inputTxt.value != '' ){

        if(inputTxt.value.length >= 5){

            if(inputTxt.value.match(regx)){
                textField.textContent = 'Good input';
                textField.style.color = "green";

            }else{
                textField.textContent = 'only numbers, letters And White space';
                textField.style.color = "red";
            }
        }else{
            textField.textContent = 'your input is less than 5 chracters';
            textField.style.color = "red";
        }
    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}

function fnameValidation(inputTxt){

    var regx = /^[a-zA-Z\s, ]+$/;
    var textField = document.getElementById("name");

    if(inputTxt.value != '' ){

        if(inputTxt.value.length >= 3){

            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "";

            }else{
                textField.textContent = '**Only characters are allowed"';
                textField.style.color = "red";
            }
        }else{
            textField.textContent = '**your product name must include more chracters';
            textField.style.color = "red";
        }
    }else{
        textField.textContent = '**Please enter your product name';
        textField.style.color = "red";
    }
}


//function lnameValidation(inputTxt){
//
//    var regx = /^[a-zA-Z\s, ]+$/;
//    var textField = document.getElementById("names");
//
//    if(inputTxt.value != '' ){
//
//        if(inputTxt.value.length >= 1){
//
//            if(inputTxt.value.match(regx)){
//                textField.textContent = '';
//                textField.style.color = "green";
//
//            }else{
//                textField.textContent = 'only characters allowded';
//                textField.style.color = "red";
//            }
//        }else{
//            textField.textContent = 'your input mut me more than two chracters';
//            textField.style.color = "red";
//        }
//    }else{
//        textField.textContent = 'your input is empty';
//        textField.style.color = "red";
//    }
//}


function priceValidation(inputTxt){

    var regx = /^\d+(\.\d{1,2})?$/;
    var textField = document.getElementById("price");

    if(inputTxt.value != '' ){

        if(inputTxt.value.match(regx)){
            textField.textContent = '';
            textField.style.color = "green";

        }else{
            textField.textContent = 'only numbers with up to 2 decimal places allowed';
            textField.style.color = "red";
        }

    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}

//
//function price(inputTxt){
//
//    var regx = /^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/.test(price);
//    var textField = document.getElementById("pho");
//
//    if(inputTxt.value != '' ){
//        if(inputTxt.value.match(regx)){
//            textField.textContent = '';
//            textField.style.color = "green";
//            }else{
//                textField.textContent = '**not valid phone number';
//                textField.style.color = "red";
//            }
//    }else{
//        textField.textContent = '**Please enter your phone number';
//        textField.style.color = "red";
//    }
//}





function passwordValidation(inputTxt){

    var regx = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}/;
    var textField = document.getElementById("pass1");

    if(inputTxt.value != '' ){
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "green";

            }else{
                textField.textContent = 'Must contain at least one number and one uppercase and lowercase letter and aleast 5 characters';
                textField.style.color = "red";
            }
    }else{
        textField.textContent = '**Password cannot be null!!';
        textField.style.color = "red";
    }
}


function cpasswordValidation(inputTxt){

    var regx =  document.getElementById("pwd").value;
    var regy =  document.getElementById("cpwd").value;
    var textField = document.getElementById("pass2");


    if(inputTxt.value != '' ){
            if(regx == regy){
                textField.textContent = '';
                textField.style.color = "green";

            }else{
                textField.textContent = '**passwords should be matching';
                textField.style.color = "red";
            }
        }else{
            textField.textContent = '**confrim password cannot be null!!';
            textField.style.color = "red";
        }
}



//       function validation(){
//             var fname=document.getElementById('f-name').value;

//           if(fname==""){
//              document.getElementById('name').innerHTML="**Please enter your firstname";
//              return false;
//           }
//           else{
//              document.getElementById('name').innerHTML="";
//           }

//           if((fname.length<=2)||(fname.length>20)){

//              document.getElementById('name').innerHTML="**User length must be between 2 and 20";
//              return false;

//           }
//           else{
//              document.getElementById('name').innerHTML="";
//           }


//           if(!isNaN(fname)){

//              document.getElementById('name').innerHTML="**Only characters are allowed";
//              return false;

//           }
//           else{
//              document.getElementById('name').innerHTML="";
//           }


//           var lname=document.getElementById('l-name').value;
//           if(lname==""){
//              document.getElementById('names').innerHTML="**Please enter your lastname";
//              return false;
//           }
//           else{
//              document.getElementById('names').innerHTML="";
//           }

//           if((lname.length<=2)||(fname.length>20)){

//              document.getElementById('names').innerHTML="**User length must be between 2 and 20";
//              return false;

//           }
//           else{
//              document.getElementById('names').innerHTML="";
//           }


//           if(!isNaN(lname)){

//              document.getElementById('names').innerHTML="**Only characters are allowed";
//              return false;

//           }
//           else{
//              document.getElementById('names').innerHTML="";
//           }

//   var detail=document.getElementById('details').value;

//     if(detail==""){
//        document.getElementById('addr').innerHTML="**Please enter your address";
//        return false;
//     }
//     else{
//        document.getElementById('addr').innerHTML="";
//     }
//     if((detail.length<=2)||(detail.length>60)){

//       document.getElementById('addr').innerHTML="**User length must be between 2 and 60S";
//       return false;

//       }
//       else{
//       document.getElementById('addr').innerHTML="";
//       }

// var val = document.getElementById('email').value;

// if (!val.match(/([A-z0-9_\-\.]){1,}\@([A-z0-9_\-\.]){1,}\.([A-Za-z]){2,4}$/))
// {
//     document.getElementById('mail').innerHTML="**enter a Valid Email";
//     return false;
// }
// else{
//     document.getElementById('mail').value = "";
// }


//     var phon=document.getElementById('phoneno').value;
//       if(phon==""){

//          document.getElementById('pho').innerHTML="**Please enter your phone number";
//          return false;
//       }
//       else{
//          document.getElementById('pho').innerHTML="";
//       }
//       if(isNaN(phon)){

//          document.getElementById('pho').innerHTML="**User must enter only digits and not characters";
//          return false;
//       }
//       else{
//          document.getElementById('pho').innerHTML="";
//       }
//       if(phon.length!=10){

//          document.getElementById('pho').innerHTML="**Phone number must be 10 digits only";
//          return false;
//       }
//       else{
//          document.getElementById('pho').innerHTML="";
//       }

//       if(!val.match("[0-9]{3}-[0-9]{2}-[0-9]{3}"))
//       {
//         document.getElementById('pho').innerHTML="**Phone number must be in valid format!!!";
//          return false;
//       }
//       else{
//          document.getElementById('pho').innerHTML="";
//       }

//       var cities=document.getElementById('city').value;
//       if(cities==""){

//      document.getElementById('cit').innerHTML="**Please enter your city";
//      return false;

//       }
//       else{
//          document.getElementById('cit').innerHTML="";
//       }

//       var stat=document.getElementById('state').value;
//       if(stat==""){

//      document.getElementById('states').innerHTML="**Please enter your state";
//      return false;

//       }
//       else{
//          document.getElementById('states').innerHTML="";
//       }

//     var code=document.getElementById('pincode').value;
//     var a = /(^\d{6}$)/;
//         if (code=="")
//         {
//             document.getElementById('pin').innerHTML="**Please enter the pincode";
//             return false;
//         }
//         else
//         {
//             document.getElementById('pin').innerHTML="";
//         }

//         if(isNaN(code)){

//         document.getElementById('pin').innerHTML="**User must enter only digits and not characters";
//         return false;

//         }
//         else{
//         document.getElementById('pin').innerHTML="";
//         }
//         if(code.length!=6){

//         document.getElementById('pin').innerHTML="**pin number must be 6 digits only";
//         return false;


//         }
//         else{
//         document.getElementById('pin').innerHTML="";
//         }

//         var fe=document.getElementById('f').Checked;
//         var ma=document.getElementById('m').checked;
//         if(ma == true) {
//                 document.getElementById("dis").innerHTML ="You have selected male any";
//                 return false;
//             }
//             else if(fe == true){
//                 document.getElementById("dis").innerHTML = "You have selected female any";
//                 return false;
//             }
//             else{
//                 document.getElementById("dis").innerHTML = "You have not selected  any";
//             }

//             var val = document.getElementById('pwd').value;
//             var ps2=document.getElementById('cpwd').value;
//             if(val=="")
//                 {
//                     document.getElementById('pass1').innerHTML="**Password can't be null!!";
//                     return false;
//                 }
//                 else{
//                 document.getElementById('pass1').value = "";
//             }

//             if (!val.match(/^[A-Za-z0-9!-*]{4,15}$/))
//             {
//                 document.getElementById('pass1').innerHTML="**Password should contain atleast 4 characters";
//                 return false;
//             }
//             else{
//                 document.getElementById('pass1').value = "";
//             }
//             if(ps2==""){

//             document.getElementById('pass2').innerHTML="**confrim password can't be null!!";
//             return false;
//             }
//             else{
//             document.getElementById('pass2').innerHTML="";
//             }
//             if(val!=ps2){

//             document.getElementById('pass2').innerHTML="**passwords should be matching";
//             return false;
//             }
//             else{
//             document.getElementById('pass2').innerHTML="";
//             }

//             if(!this.formreg.agree.checked)
//             {
//             document.getElementById('box').innerHTML="**you must agree to the privacy policy";
//             return false;
//             }
//             else{
//             document.getElementById('box').innerHTML="";
//             }

// }




