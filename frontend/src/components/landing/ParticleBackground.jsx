import { useEffect, useRef } from 'react'

function ParticleBackground() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    let animationFrameId
    let stars = []
    let shootingStars = []
    let nebulaClouds = []

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = document.documentElement.scrollHeight
    }

    const createStars = () => {
      stars = []
      // Many small stars
      const numStars = Math.floor((canvas.width * canvas.height) / 3000)
      
      for (let i = 0; i < numStars; i++) {
        const type = Math.random()
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: type < 0.7 ? Math.random() * 1.5 + 0.5 : // Small stars (70%)
                type < 0.95 ? Math.random() * 2 + 1.5 :   // Medium stars (25%)
                Math.random() * 3 + 2.5,                   // Bright stars (5%)
          twinkleSpeed: Math.random() * 0.03 + 0.01,
          twinkleOffset: Math.random() * Math.PI * 2,
          baseOpacity: type < 0.7 ? Math.random() * 0.4 + 0.2 :
                       type < 0.95 ? Math.random() * 0.5 + 0.4 :
                       Math.random() * 0.3 + 0.7,
          color: getStarColor(type),
          // Parallax movement
          depth: Math.random() * 0.5 + 0.1
        })
      }

      // Create nebula clouds
      nebulaClouds = []
      const numClouds = 5
      for (let i = 0; i < numClouds; i++) {
        nebulaClouds.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 300 + 200,
          color: getNebulaColor(),
          opacity: Math.random() * 0.08 + 0.02,
          speedX: (Math.random() - 0.5) * 0.1,
          speedY: (Math.random() - 0.5) * 0.1
        })
      }
    }

    const getStarColor = (type) => {
      if (type < 0.5) return { r: 255, g: 255, b: 255 } // White
      if (type < 0.65) return { r: 200, g: 220, b: 255 } // Blue-white
      if (type < 0.8) return { r: 255, g: 240, b: 220 } // Warm white
      if (type < 0.9) return { r: 150, g: 180, b: 255 } // Blue
      if (type < 0.95) return { r: 180, g: 130, b: 255 } // Purple
      return { r: 100, g: 200, b: 255 } // Cyan (rare bright)
    }

    const getNebulaColor = () => {
      const colors = [
        { r: 99, g: 102, b: 241 },   // Indigo
        { r: 168, g: 85, b: 247 },   // Purple
        { r: 59, g: 130, b: 246 },   // Blue
        { r: 139, g: 92, b: 246 },   // Violet
        { r: 34, g: 211, b: 238 },   // Cyan
      ]
      return colors[Math.floor(Math.random() * colors.length)]
    }

    const createShootingStar = () => {
      if (Math.random() < 0.003 && shootingStars.length < 3) { // Rare shooting stars
        const startX = Math.random() * canvas.width
        const startY = Math.random() * canvas.height * 0.5
        shootingStars.push({
          x: startX,
          y: startY,
          length: Math.random() * 100 + 50,
          speed: Math.random() * 15 + 10,
          angle: Math.PI / 4 + (Math.random() - 0.5) * 0.3,
          opacity: 1,
          tail: []
        })
      }
    }

    let time = 0
    const drawFrame = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      time += 0.016

      // Draw nebula clouds (background)
      nebulaClouds.forEach(cloud => {
        cloud.x += cloud.speedX
        cloud.y += cloud.speedY

        // Wrap around
        if (cloud.x < -cloud.radius) cloud.x = canvas.width + cloud.radius
        if (cloud.x > canvas.width + cloud.radius) cloud.x = -cloud.radius
        if (cloud.y < -cloud.radius) cloud.y = canvas.height + cloud.radius
        if (cloud.y > canvas.height + cloud.radius) cloud.y = -cloud.radius

        const gradient = ctx.createRadialGradient(
          cloud.x, cloud.y, 0,
          cloud.x, cloud.y, cloud.radius
        )
        gradient.addColorStop(0, `rgba(${cloud.color.r}, ${cloud.color.g}, ${cloud.color.b}, ${cloud.opacity})`)
        gradient.addColorStop(0.5, `rgba(${cloud.color.r}, ${cloud.color.g}, ${cloud.color.b}, ${cloud.opacity * 0.3})`)
        gradient.addColorStop(1, `rgba(${cloud.color.r}, ${cloud.color.g}, ${cloud.color.b}, 0)`)
        
        ctx.beginPath()
        ctx.arc(cloud.x, cloud.y, cloud.radius, 0, Math.PI * 2)
        ctx.fillStyle = gradient
        ctx.fill()
      })

      // Draw stars
      stars.forEach(star => {
        // Twinkling effect
        const twinkle = Math.sin(time * star.twinkleSpeed * 60 + star.twinkleOffset)
        const opacity = star.baseOpacity * (0.5 + twinkle * 0.5)
        
        // Slight movement (parallax)
        star.x += star.depth * 0.05
        if (star.x > canvas.width) star.x = 0

        const { r, g, b } = star.color

        // Star core
        ctx.beginPath()
        ctx.arc(star.x, star.y, star.size * 0.5, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${opacity})`
        ctx.fill()

        // Star glow
        if (star.size > 1.5) {
          const glowGradient = ctx.createRadialGradient(
            star.x, star.y, 0,
            star.x, star.y, star.size * 3
          )
          glowGradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${opacity * 0.8})`)
          glowGradient.addColorStop(0.3, `rgba(${r}, ${g}, ${b}, ${opacity * 0.3})`)
          glowGradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`)
          
          ctx.beginPath()
          ctx.arc(star.x, star.y, star.size * 3, 0, Math.PI * 2)
          ctx.fillStyle = glowGradient
          ctx.fill()
        }

        // Cross flare for bright stars
        if (star.size > 2.5) {
          ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${opacity * 0.5})`
          ctx.lineWidth = 0.5
          const flareLength = star.size * 4
          
          ctx.beginPath()
          ctx.moveTo(star.x - flareLength, star.y)
          ctx.lineTo(star.x + flareLength, star.y)
          ctx.stroke()
          
          ctx.beginPath()
          ctx.moveTo(star.x, star.y - flareLength)
          ctx.lineTo(star.x, star.y + flareLength)
          ctx.stroke()
        }
      })

      // Create and draw shooting stars
      createShootingStar()
      
      shootingStars = shootingStars.filter(star => {
        star.x += Math.cos(star.angle) * star.speed
        star.y += Math.sin(star.angle) * star.speed
        star.opacity -= 0.015

        if (star.opacity <= 0) return false

        // Draw shooting star trail
        const tailLength = star.length
        const tailX = star.x - Math.cos(star.angle) * tailLength
        const tailY = star.y - Math.sin(star.angle) * tailLength

        const gradient = ctx.createLinearGradient(tailX, tailY, star.x, star.y)
        gradient.addColorStop(0, `rgba(255, 255, 255, 0)`)
        gradient.addColorStop(0.8, `rgba(200, 220, 255, ${star.opacity * 0.5})`)
        gradient.addColorStop(1, `rgba(255, 255, 255, ${star.opacity})`)

        ctx.beginPath()
        ctx.moveTo(tailX, tailY)
        ctx.lineTo(star.x, star.y)
        ctx.strokeStyle = gradient
        ctx.lineWidth = 2
        ctx.lineCap = 'round'
        ctx.stroke()

        // Head glow
        const headGradient = ctx.createRadialGradient(
          star.x, star.y, 0,
          star.x, star.y, 8
        )
        headGradient.addColorStop(0, `rgba(255, 255, 255, ${star.opacity})`)
        headGradient.addColorStop(1, `rgba(200, 220, 255, 0)`)
        
        ctx.beginPath()
        ctx.arc(star.x, star.y, 8, 0, Math.PI * 2)
        ctx.fillStyle = headGradient
        ctx.fill()

        return star.x < canvas.width + 100 && star.y < canvas.height + 100
      })

      animationFrameId = requestAnimationFrame(drawFrame)
    }

    resizeCanvas()
    createStars()
    drawFrame()

    const handleResize = () => {
      resizeCanvas()
      createStars()
    }

    window.addEventListener('resize', handleResize)

    return () => {
      cancelAnimationFrame(animationFrameId)
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ opacity: 1 }}
    />
  )
}

export default ParticleBackground
