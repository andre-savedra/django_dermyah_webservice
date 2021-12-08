var tabela = document.getElementById("tableFiles");
var linhas = tabela.querySelectorAll("tr");
var netChoose = document.querySelector("#netChoose");
var message = document.querySelector("#error_message");
message.style.display = "none";	
var btn_submit = document.querySelector(".final_button");
btn_submit.style.backgroundColor = "red";


for (var i = 0; i < linhas.length; i++) {
    var linha = linhas[i];
    linha.addEventListener("click", function() {
        selLinha(this, false);
    });
}

function selLinha(linha, multiplos) {
    if (!multiplos) {
        var linhas_ = linha.parentElement.getElementsByTagName("tr");
        for (var i = 0; i < linhas_.length; i++) {
            var linha_ = linhas_[i];
            linha_.classList.remove("selecionado");
        }
    }
    linha.classList.toggle("selecionado");
    putField(linha);
}

function putField(linha) {
    let val = linha.querySelector(".nameNetLine").innerHTML;
    netChoose.value = val;
}

function restoreWifi(){
   
    let request = new XMLHttpRequest();    
    //RESPOSTA ASSÍNCRONA
    request.onreadystatechange = function (){
        //FINALIZOU A REQUISIÇÃO
        if(request.readyState === 4){
			
			if(request.status === 200){
				
				alert("Solicitação Atendida");
				window.location.assign("mainPage");
			}
			else{
				alert("Problema ao atender pedido!");
				window.location.assign("mainPage");
			}
				
        }
    };

    request.open('GET', '/reset', true);    
    request.send();        
       
}
console.log("JESUS2");


function check(){
	event.preventDefault();	
	
	let name = document.querySelector("#netChoose");
	let p1 = document.querySelector(".pswd1");
	let p2 = document.querySelector(".pswd2");
	
	let name_value = name.value;
	let p1_value = p1.value;
	let p2_value = p2.value;
	
	if((name_value === "") || (name_value === null))
	{
		//console.log("esta diferente...");
		btn_submit.setAttribute("disabled", "disabled");
		btn_submit.style.backgroundColor = "red";
		message.style.display = "block";
		message.innerHTML = "<p>Selecione o nome da rede Wifi primeiro!</p>";
		p1.style.backgroundColor = "#ffddd9";
		p2.style.backgroundColor = "#ffddd9";		
	}
	//name ok
	else
	{
		//password ok
		if((p1_value === p2_value) && (p1_value.length >= 8))
		{
			btn_submit.removeAttribute("disabled");
			btn_submit.style.background = "linear-gradient( 135deg, rgba(110, 172, 134, 0.294), rgba(112, 167, 107, 0.87))";
			message.style.display = "none";		
			p1.style.backgroundColor = "white";
			p2.style.backgroundColor = "white";
		}		
		else
		{
			//console.log("esta diferente...");
			btn_submit.setAttribute("disabled", "disabled");
			btn_submit.style.backgroundColor = "red";
			message.style.display = "block";
			message.innerHTML = "<p>Senhas diferentes ou menores que 8 caracteres!</p>";
			p1.style.backgroundColor = "#ffddd9";
			p2.style.backgroundColor = "#ffddd9";		
		}			
	}	
}



function load(){
   
    let request = new XMLHttpRequest();    
    //RESPOSTA ASSÍNCRONA
    request.onreadystatechange = function (){
        //FINALIZOU A REQUISIÇÃO
        if(request.readyState === 4){
			
			if(request.status === 200){
				
				alert("Solicitação Atendida");
				window.location.assign("mainPage");
			}
			else{
				alert("Problema ao atender pedido!");
				window.location.assign("mainPage");
			}
				
        }
    };

    request.open('GET', '/arduino', true);    
    request.send();        
       
}





