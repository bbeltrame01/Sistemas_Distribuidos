import React from 'react';
// https://www.npmjs.com/package/react-fade-in
import FadeIn from 'react-fade-in';

import './App.css';
// Images
import Castle from './img/castle.png';
import Crown from './img/crown.png';
import General from './img/general.png';

function App() {
  const API = `http://localhost:4000/evento`; // Atualizar API
  const server = "server";
  const clients = ["1.1.1.1","2.2.2.2","3.3.3.3"]; // Atualizar endereço de clients

  const buscaEventos = () =>{    
    fetch(API)
    .then(response => response.json())
    .then(response => {
      response.forEach( function (el, idx) { 
        setTimeout(() => {
        if(el.valor === "conectado" && el.origem !== server){
          document.getElementById(el.origem).innerHTML = "IP: "+el.origem;
          document.getElementById("valorClient"+el.origem).innerHTML = el.valor;                 
        }
        else{
          if(el.origem === server){
            document.getElementById("valorClient"+el.destino).innerHTML = el.valor;
          }else{
            var node = document.createElement("LI");
            node.appendChild(document.createTextNode(el.destino+": "+el.valor));
            document.getElementById("vDestino"+el.origem).appendChild(node);
          }       
        }
        if(el.traidor === "1"){
          document.getElementById("traidor"+el.origem).style = "background-color: red";
        }
      }, 1000*idx);     
      });
    })
  };
  
  return (
    <>
      <div className="Header">
        <button onClick={() => buscaEventos()}>Atualizar</button>
      </div>
      <div className="Content">
        <img id={"traidor"+server} width="100" src={Crown} alt="crown" />
        <FadeIn transitionDuration={1000}>
          <div className="Generais">
            <div className="General">
              <p id={"valorClient"+clients[0]}></p>
              <img id={"traidor"+clients[0]} width="100" src={General} alt="client1" />              
              <ul id={"vDestino"+clients[0]}>
                <li id={clients[0]}></li>
              </ul>
            </div>
            <div className="General">
              <p id={"valorClient"+clients[1]}></p>
              <img id={"traidor"+clients[1]} width="100" src={General} alt="client2" />
              <ul id={"vDestino"+clients[1]}>
                <li id={clients[1]}></li>
              </ul>
            </div>
            <div className="General" id='cliente3'>
              <p id={"valorClient"+clients[2]}></p>
              <img id={"traidor"+clients[2]} width="100" src={General} alt="client3" />
              <ul id={"vDestino"+clients[2]}>
                <li id={clients[2]}></li>
              </ul>
            </div>
          </div>
        </FadeIn>
        <img className="Image" width="250" src={Castle} alt="castle" />
      </div>
    </>
  );
}

export default App;
