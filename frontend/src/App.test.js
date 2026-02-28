import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders Kitchen API Demo heading", () => {
  render(<App />);
  const heading = screen.getByText(/Kitchen API Demo/i);
  expect(heading).toBeInTheDocument();
});
