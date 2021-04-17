import React from "react";
import NavigationBar from "./NavigationBar";
import JumboHeader from "./wordspage/JumboHeader";
import WordTable from "./wordspage/WordTable";

import styles from "./WordsPage.module.css";

export default function WordsPage({ srcLang, destLang }) {
  return (
    <>
      <NavigationBar />
      <div className={styles.container}>
        <JumboHeader srcLang={srcLang} destLang={destLang} />
	<hr/>
        <WordTable srcLang={srcLang} destLang={destLang} />
      </div>
    </>
  );
}
