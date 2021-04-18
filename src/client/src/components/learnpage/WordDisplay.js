import React from "react";
import styles from "./styles/WordDisplay.module.css";

export default function WordDisplay({ word, srcLang, destLang }) {
  return (
    <>
      <p>#{word.rank}</p>
      <p className={styles.langLabel}>{srcLang}</p>
      <h1>{word.text}</h1>
      <br />
      <p className={styles.langLabel}>{destLang}</p>
      <p className={styles.translations}>
        {word.translations.slice(0, 4).join(", ")}
      </p>
    </>
  );
}
