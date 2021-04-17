import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import WordsPage from "./components/WordsPage";
import LearnPage from "./components/LearnPage";

function App() {
  return (
    <Router>
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
          <LearnPage srcLang="french" destLang="english" />
        </Route>
        <Route path="/french">
          <WordsPage srcLang="french" destLang="english" />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
