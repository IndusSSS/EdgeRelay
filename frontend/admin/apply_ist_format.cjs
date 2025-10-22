const fs = require('fs');

// Clean IST formatDate function
const istFormatDate = `formatDate(date) {
      if (!date) return 'Never'
      
      const dt = new Date(date)
      
      // Convert to IST (UTC + 5:30 hours)
      const istTime = new Date(dt.getTime() + (5.5 * 60 * 60 * 1000))
      
      // Format in Indian style: DD/MM/YYYY, H:MM:SS AM/PM IST
      const day = istTime.getUTCDate().toString().padStart(2, '0')
      const month = (istTime.getUTCMonth() + 1).toString().padStart(2, '0')
      const year = istTime.getUTCFullYear()
      const hours = istTime.getUTCHours()
      const minutes = istTime.getUTCMinutes().toString().padStart(2, '0')
      const seconds = istTime.getUTCSeconds().toString().padStart(2, '0')
      const ampm = hours >= 12 ? 'PM' : 'AM'
      const displayHours = hours % 12 || 12
      
      return \`\${day}/\${month}/\${year}, \${displayHours}:\${minutes}:\${seconds} \${ampm} IST\`
    }`

// Function to safely replace formatDate in a Vue file
function updateFormatDate(filePath) {
  if (!fs.existsSync(filePath)) {
    console.log('File not found: ' + filePath)
    return false
  }
  
  let content = fs.readFileSync(filePath, 'utf8')
  
  // Find the formatDate function using a more precise regex
  const formatDateRegex = /formatDate\(date\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}/
  
  if (!formatDateRegex.test(content)) {
    console.log('formatDate function not found in: ' + filePath)
    return false
  }
  
  // Replace the formatDate function
  const updatedContent = content.replace(formatDateRegex, istFormatDate)
  
  // Write back
  fs.writeFileSync(filePath, updatedContent)
  console.log('✅ Updated: ' + filePath)
  return true
}

// Update the Vue files
const files = [
  './src/views/Devices.vue',
  './src/views/DevicesIntegrated.vue'
]

let successCount = 0
files.forEach(file => {
  if (updateFormatDate(file)) {
    successCount++
  }
})

console.log('\\n🎉 Successfully updated ' + successCount + '/' + files.length + ' files with IST format!')
