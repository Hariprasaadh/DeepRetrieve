import { useEffect, useRef } from 'react'

function ParticleBackground() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    let animationFrameId
    let stars = []
    let lastTime = 0
    const FPS_LIMIT = 30 // Limit to 30fps for performance

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    const createStars = () => {
      stars = []
      // Reduced star count for performance (max 150 stars)
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
      // Limit FPS for performance
      if (timestamp - lastTime < 1000 / FPS_LIMIT) {
        animationFrameId = requestAnimationFrame(drawFrame)
        return
      }
      lastTime = timestamp
      
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      time += 0.033

      // Draw stars (simplified - no gradients)
      stars.forEach(star => {
        const twinkle = Math.sin(time * star.twinkleSpeed * 60 + star.twinkleOffset)
        const opacity = star.baseOpacity * (0.6 + twinkle * 0.4)
        
        ctx.beginPath()
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`
        ctx.fill()

        // Simple glow for bright stars only (10% of stars)
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

    // Debounced resize handler
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
