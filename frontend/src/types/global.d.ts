// Global type declarations

declare global {
  interface Window {
    Hammer: any
  }
  
  interface HTMLElement {
    _wheelHandler?: (e: WheelEvent) => void
  }
}

export {}