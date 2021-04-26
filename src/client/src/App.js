import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import NavigationBar from "./components/global/NavigationBar";
import HomePage from "./components/homepage/HomePage";
import WordsPage from "./components/wordspage/WordsPage";
import LearnPage from "./components/learnpage/LearnPage";

function App() {
  return (
    <Router>
      <NavigationBar />
      <Switch>
        <Route exact path="/">
          <HomePage />
        </Route>
        <Route path="/spanish/learn">
          <LearnPage srcLang="spanish" destLang="english" />
        </Route>
        <Route path="/spanish">
          <WordsPage srcLang="spanish" destLang="english" />
        </Route>
        <Route path="/french/learn">
          <LearnPage srcLang="french" destLang="english" romanize={false} />
        </Route>
        <Route path="/french">
          <WordsPage srcLang="french" destLang="english" romanize={false} />
        </Route>
        <Route path="/german/learn">
          <LearnPage srcLang="german" destLang="english" romanize={false} />
        </Route>
        <Route path="/german">
          <WordsPage srcLang="german" destLang="english" romanize={false} />
        </Route>
        <Route path="/italian/learn">
          <LearnPage srcLang="italian" destLang="english" romanize={false} />
        </Route>
        <Route path="/italian">
          <WordsPage srcLang="italian" destLang="english" romanize={false} />
        </Route>
        <Route path="/italian/learn">
          <LearnPage srcLang="italian" destLang="english" romanize={false} />
        </Route>
        <Route path="/italian">
          <WordsPage srcLang="italian" destLang="english" romanize={false} />
        </Route>
        <Route path="/dutch/learn">
          <LearnPage srcLang="dutch" destLang="english" romanize={false} />
        </Route>
        <Route path="/dutch">
          <WordsPage srcLang="dutch" destLang="english" romanize={false} />
        </Route>
        <Route path="/russian/learn">
          <LearnPage srcLang="russian" destLang="english" romanize={true} />
        </Route>
        <Route path="/russian">
          <WordsPage srcLang="russian" destLang="english" romanize={true} />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
