import React from "react";
import styles from "./styles/WordDisplay.module.css";

export default function WordDisplay({ word }) {
  return (
    <>
      <p>#{word.rank}</p>
      <p className={styles.langLabel}>SPANISH</p>
      <h1>{word.text}</h1>
      <br />
      <p className={styles.langLabel}>ENGLISH</p>
      <p className={styles.translations}>
        {word.translations.slice(0, 4).join(", ")}
      </p>
    </>
  );
}
