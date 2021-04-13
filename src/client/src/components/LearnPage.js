import React from "react";
import NavigationBar from "./NavigationBar";
import WordSelector from "./learnpage/WordSelector";

export default function LearnPage({ srcLang, destLang }) {
  return (
    <>
      <NavigationBar />
      <WordSelector srcLang={srcLang} destLang={destLang} />
    </>
  );
}
