import React from "react";
import { Container, Navbar, Jumbotron, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <>
      <Container bg="white">
        <Navbar bg="white" expand="lg">
          <Navbar.Brand as={Link} to="/">
            milnomen
          </Navbar.Brand>
        </Navbar>
        <Jumbotron
          style={{ backgroundColor: "#fff", padding: 70, marginBottom: 0 }}
        >
          <h1>Reach 80% fluency</h1>
          <h2>in just one thousand words</h2>
          <p style={{ marginTop: 25 }}>
            Study the top 1000 words in any language - now with sentences!
          </p>
          <p style={{ marginTop: 80 }}>
            <Button style={{ paddingLeft: 20, paddingRight: 20 }}>
              Start learning
            </Button>
          </p>
        </Jumbotron>
      </Container>

      <Container fluid style={{ backgroundColor: "#eee" }}>
        <p style={{ padding: 10, textAlign: "center" }}>
          Check out 800,000+ sentences over 14 languages
        </p>
      </Container>
    </>
  );
}
