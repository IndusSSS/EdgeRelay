const fs = require('fs');

// Correctly parse UTC timestamp and convert to IST
const correctedFormatDate = `formatDate(date) {
      if (!date) return 'Never'
      
      // Parse as UTC timestamp (add Z if not present)
      const utcDate = new Date(date.endsWith('Z') ? date : date + 'Z')
      
      // Convert to IST (UTC + 5:30 hours)
      const istTime = new Date(utcDate.getTime() + (5.5 * 60 * 60 * 1000))
      
      // Format in Indian style: DD/MM/YYYY, H:MM:SS AM/PM
      const day = istTime.getUTCDate().toString().padStart(2, '0')
      const month = (istTime.getUTCMonth() + 1).toString().padStart(2, '0')
      const year = istTime.getUTCFullYear()
      const hours = istTime.getUTCHours()
      const minutes = istTime.getUTCMinutes().toString().padStart(2, '0')
      const seconds = istTime.getUTCSeconds().toString().padStart(2, '0')
      const ampm = hours >= 12 ? 'PM' : 'AM'
      const displayHours = hours % 12 || 12
      
      return \`\${day}/\${month}/\${year}, \${displayHours}:\${minutes}:\${seconds} \${ampm}\`
    }`

// Test the corrected function
function testFormatDate(date) {
  if (!date) return 'Never'
  
  const utcDate = new Date(date.endsWith('Z') ? date : date + 'Z')
  const istTime = new Date(utcDate.getTime() + (5.5 * 60 * 60 * 1000))
  
  const day = istTime.getUTCDate().toString().padStart(2, '0')
  const month = (istTime.getUTCMonth() + 1).toString().padStart(2, '0')
  const year = istTime.getUTCFullYear()
  const hours = istTime.getUTCHours()
  const minutes = istTime.getUTCMinutes().toString().padStart(2, '0')
  const seconds = istTime.getUTCSeconds().toString().padStart(2, '0')
  const ampm = hours >= 12 ? 'PM' : 'AM'
  const displayHours = hours % 12 || 12
  
  return \`\${day}/\${month}/\${year}, \${displayHours}:\${minutes}:\${seconds} \${ampm}\`
}

console.log('Testing CORRECTED UTC parsing:')
const testDate = '2025-10-02T02:40:21.000000'
console.log('UTC:', testDate)
console.log('IST:', testFormatDate(testDate))
console.log('Expected: 02/10/2025, 8:10:21 AM')
console.log('')

// Update Vue files
function updateFormatDate(filePath) {
  if (!fs.existsSync(filePath)) {
    console.log('File not found: ' + filePath)
    return false
  }
  
  let content = fs.readFileSync(filePath, 'utf8')
  const formatDateRegex = /formatDate\(date\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}/
  
  if (!formatDateRegex.test(content)) {
    console.log('formatDate function not found in: ' + filePath)
    return false
  }
  
  const updatedContent = content.replace(formatDateRegex, correctedFormatDate)
  fs.writeFileSync(filePath, updatedContent)
  console.log('✅ Updated: ' + filePath)
  return true
}

const files = [
  './frontend/admin/src/views/Devices.vue',
  './frontend/admin/src/views/DevicesIntegrated.vue'
]

let successCount = 0
files.forEach(file => {
  if (updateFormatDate(file)) {
    successCount++
  }
})

console.log('\\n🎉 Successfully updated ' + successCount + '/' + files.length + ' files with CORRECT UTC parsing!')
