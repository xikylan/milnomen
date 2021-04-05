import React from "react";

import NavigationBar from "./NavigationBar";
import JumboHeader from "./wordspage/JumboHeader";
import WordTable from "./wordspage/WordTable";

export default function SpanishWordsPage() {
  return (
    <>
      <NavigationBar />
      <JumboHeader srcLang="spanish" destLang="english" />
      <WordTable srcLang="spanish" destLang="english" />
    </>
  );
}
