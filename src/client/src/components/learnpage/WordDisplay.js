import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import styles from "./styles/WordDisplay.module.css";

export default function WordDisplay({ word, srcLang, destLang, romanize }) {
  const [audio, setAudio] = useState(null);

  //  useEffect(() => {
  //    import(`../../assets/audio/${srcLang}/${word.text}.mp3`)
  //      .then((sound) => {
  //        setAudio(new Audio(sound["default"]));
  //      })
  //      .catch((error) => console.log(error.message));
  //  }, [srcLang, word.text]);

  return (
    <>
      <p>#{word.rank}</p>
      <p className={styles.langLabel}>{srcLang}</p>
      <h1 className={styles.word}>{word.text}</h1>
      {romanize ? <p className={styles.romanized}>{word.romanized}</p> : null}
      <hr />
      <p className={styles.langLabel}>{destLang}</p>
      <p className={styles.translations}>
        {word.translations.slice(0, 3).join(", ")}
      </p>
      <Button
        variant="light"
        onClick={() => {
          audio.play();
        }}
      >
        Listen
      </Button>
    </>
  );
}
