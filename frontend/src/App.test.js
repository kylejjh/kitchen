import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders Kitchen API Demo heading", () => {
  render(<App />);
  expect(screen.getByText(/Kitchen API Demo/i)).toBeInTheDocument();
});

test("renders /demo/one endpoint heading", () => {
  render(<App />);
  expect(screen.getByText("/demo/one")).toBeInTheDocument();
});

test("renders /demo/two endpoint heading", () => {
  render(<App />);
  expect(screen.getByText("/demo/two")).toBeInTheDocument();
});

test("renders /demo/three endpoint heading", () => {
  render(<App />);
  expect(screen.getByText("/demo/three")).toBeInTheDocument();
});
