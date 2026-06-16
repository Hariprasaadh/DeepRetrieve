// Purpose: Ambient canvas particle effect renderer.
// Responsibilities: Runs a lightweight particle simulation loop inside an HTML5 canvas element, 
// managing canvas resizing, interactive mouse tracking, and low-overhead frame rendering.

import { useEffect, useRef } from 'react'


function ParticleBackground() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    let animationFrameId
    let stars = []
    let lastTime = 0
    const FPS_LIMIT = 30 // Target refresh rate to balance visual smoothness and GPU load

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    const createStars = () => {
      stars = []
      // Dynamically scale particle count based on screen real estate up to a safety ceiling
      const numStars = Math.min(150, Math.floor((canvas.width * canvas.height) / 8000))
      
      for (let i = 0; i < numStars; i++) {
        const type = Math.random()
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: type < 0.8 ? Math.random() * 1.2 + 0.3 : Math.random() * 2 + 1,
          twinkleSpeed: Math.random() * 0.02 + 0.005,
          twinkleOffset: Math.random() * Math.PI * 2,
          baseOpacity: Math.random() * 0.5 + 0.3,
          isBright: type > 0.9
        })
      }
    }

    let time = 0
    const drawFrame = (timestamp) => {
      // Throttle canvas frame updates to stay within target FPS budget
      if (timestamp - lastTime < 1000 / FPS_LIMIT) {
        animationFrameId = requestAnimationFrame(drawFrame)
        return
      }
      lastTime = timestamp
      
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      time += 0.033

      stars.forEach(star => {
        const twinkle = Math.sin(time * star.twinkleSpeed * 60 + star.twinkleOffset)
        const opacity = star.baseOpacity * (0.6 + twinkle * 0.4)
        
        ctx.beginPath()
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`
        ctx.fill()

        if (star.isBright) {
          ctx.beginPath()
          ctx.arc(star.x, star.y, star.size * 2, 0, Math.PI * 2)
          ctx.fillStyle = `rgba(150, 170, 255, ${opacity * 0.3})`
          ctx.fill()
        }
      })

      animationFrameId = requestAnimationFrame(drawFrame)
    }

    resizeCanvas()
    createStars()
    animationFrameId = requestAnimationFrame(drawFrame)

    let resizeTimeout
    const handleResize = () => {
      clearTimeout(resizeTimeout)
      resizeTimeout = setTimeout(() => {
        resizeCanvas()
        createStars()
      }, 250)
    }

    window.addEventListener('resize', handleResize)

    return () => {
      cancelAnimationFrame(animationFrameId)
      clearTimeout(resizeTimeout)
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
    />
  )
}

export default ParticleBackground
