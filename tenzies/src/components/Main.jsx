import { useState,useEffect } from "react";
import {nanoid} from "nanoid";
import Confetti from "react-confetti";
import Die from "./Die";
export default function Main(){
    const [dice, setDice] = useState(()=>generateDice());
    const [counter,setCounter]=useState(0)
    const [bestScore,setBestScore]=useState(()=>localStorage.getItem("bestScore")||null)
    const [msg,setMsg]=useState(false)
    
    const diceElements = dice.map((obj) => (
      <Die
        key={obj.id}
        value={obj.value}
        isHeld={obj.isHeld}
        hold={() => hold(obj.id)}
      />
    ));

    const gameWon =
      dice.every((die) => die.isHeld) &&
      dice.every((die) => die.value === dice[0].value);
    
      useEffect(() => {
        if (gameWon) {
          const bestScore = localStorage.getItem("bestScore");
          if (!bestScore || counter < parseInt(bestScore)) {
            localStorage.setItem("bestScore", counter);
            setBestScore(counter)
            setMsg(true)
            setTimeout(()=>
            setMsg(false),5000)
          }
        }
      }, [gameWon]);

    function generateDice() {
      return new Array(10).fill(0)
      .map(()=>({
        value: Math.ceil(Math.random()*6),
        isHeld : false,
        id:nanoid()}))
    }
    
    function rollDice(){
        if(gameWon){
            if(!bestScore || counter<parseInt(bestScore)){
              localStorage.setItem("bestScore",counter)
              setBestScore(counter)
            }    
            setDice(generateDice())
            setCounter(0)
        }
        else{
            setCounter(prev=>prev+1)
            setDice((prev) =>
              prev.map((die) =>
                die.isHeld
                  ? die
                  : { ...die, value: Math.ceil(Math.random() * 6) }
              )
            );
        }
        
    }

    function hold(id){
        setDice((prev)=>prev.map(die=> (die.id===id?{...die,isHeld:!die.isHeld}:die)))
    }
    
    return (
      <main>
        {gameWon && <Confetti />}
        <h1>Tenzies</h1>
        <p>
          Roll until all dice are the same. Click each die to freeze it at its
          current value between rolls.
        </p>
        <p className="counter">
          {gameWon
            ? `You won the game after ${counter} tries`
            : `Tries: ${counter}`}
        </p>
        {msg && <p className="msg">New Best Score!</p>}
        <div className="bestscore">{bestScore && <p>Best Score:{bestScore}</p>}</div>
        <div className="die">{diceElements}</div>
        <button onClick={rollDice} className="rollbutton">
          {gameWon ? "New Game" : "Roll"}
        </button>
      </main>
    );
}