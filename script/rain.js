function random(min = 0, max = 1) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

class Entity {
  static showAll(list) {
    for (let i = 0; i < list.length; i++) {
      if (!list[i].show()) {
        list.splice(i, 1);
      }
    }
  }
  constructor(x, y, ctx) {
    this.pos = { x, y };
    this.ctx = ctx;
  }
  show() {
    if (this.update()) {
      this.draw();
      return true;
    } else {
      return false;
    }
  }
}

class Strand extends Entity {
  constructor(x, canvas, ctx) {
    super(x, Char.height, ctx);
    this.canvas = canvas;
    this.chars = [];
  }
  update() {
    if (
      this.chars.length < 1 ||
      this.chars[this.chars.length - 1].pos.y < this.canvas.height * 2
    ) {
      this.chars.push(new Char(this.pos.x, this.pos.y, this.ctx));
      this.pos.y += Char.height;
      return true;
    } else {
      return false;
    }
  }
  draw() {
    Entity.showAll(this.chars);
  }
}

class Char extends Entity {
  static size = 11;
  static width = 11;
  static height = 16;
  constructor(x, y, ctx) {
    super(x, y, ctx);
    this.charList = "UX01ZWLH-";
    this.alpha = 0.2;
    this.randomizeCharVal();
  }
  randomizeCharVal() {
    this.val = this.charList[random(0, this.charList.length - 1)];
  }
  update() {
    if (random(0, 100) < 5) {
      this.randomizeCharVal();
    }
    this.alpha *= 0.96;
    return this.alpha >= 0.01 ? true : false;
  }
  draw() {
    this.ctx.font = Char.size + "px 'Courier New'";
    this.ctx.shadowOffsetX = 1;
    this.ctx.shadowOffsetY = 1;
    this.ctx.shadowColor = "rgba(0, 0, 0, 100)";
    this.ctx.fillStyle = `rgba(0,255,0,${this.alpha})`;
    this.ctx.fillText(this.val, this.pos.x, this.pos.y);
  }
}

class MatrixRain {
  constructor(element, width, height, flowRate, fps) {
    this.canvas = element;
    this.setCanvasDimensions(width, height);
    this.flowRate = flowRate;
    this.ctx = this.canvas.getContext("2d");
    this.ctx.translate(this.canvas.width, 0);
    this.ctx.scale(-1, 1);
    this.strands = [];
    this.interval = setInterval(() => {
      this.run();
    }, 1000 / fps);
  }

  setCanvasDimensions(width, height) {
    this.canvas.width = width;
    this.canvas.height = height;
    this.columns = Math.ceil(this.canvas.width / Char.width);
  }

  run() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.fillStyle = getComputedStyle(
      document.documentElement,
    ).getPropertyValue("--primary");
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    let column, available;
    for (let i = 0; i < this.flowRate; i++) {
      column = random(0, this.columns);
      available = true;
      for (let i = 0; i < this.strands.length; i++) {
        if (
          this.strands[i].pos.x == column * Char.width &&
          this.strands[i].pos.y <= this.canvas.height
        ) {
          available = false;
        }
      }
      if (available) {
        this.strands.push(
          new Strand(column * Char.width, this.canvas, this.ctx),
        );
      }
    }
    Entity.showAll(this.strands);
  }
}
