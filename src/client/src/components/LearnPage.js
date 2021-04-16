import React from "react";
import NavigationBar from "./NavigationBar";
import WordSelector from "./learnpage/WordSelector";

import styles from "./LearnPage.module.css";

export default function LearnPage({ srcLang, destLang }) {
  return (
    <>
      <NavigationBar />
      <div className={styles.container}>
        <WordSelector srcLang={srcLang} destLang={destLang} />
      </div>
    </>
  );
}
