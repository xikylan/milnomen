import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import SpanishWordsPage from "./components/SpanishWordsPage";
import SpanishSentencesPage from "./components/SpanishSentencesPage";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route path="/es/study" component={SpanishSentencesPage} />
        <Route path="/es" component={SpanishWordsPage} />
      </Switch>
    </Router>
  );
}

export default App;
