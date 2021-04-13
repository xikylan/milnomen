import React from "react";
import styles from "./styles/WordDisplay.module.css";

export default function WordDisplay({ word }) {
  return (
    <>
      <p>#{word.rank}</p>
      <h1>{word.text}</h1>
      <hr />
      <p>English:</p>
      <p className={styles.translations}>{word.translations.join(", ")}</p>
      <hr />
    </>
  );
}
