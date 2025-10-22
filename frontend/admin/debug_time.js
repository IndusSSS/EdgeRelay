// Debug the time conversion issue
const testDate = '2025-10-02T02:40:21.000000'
console.log('Original UTC:', testDate)

const dt = new Date(testDate)
console.log('Date object:', dt)
console.log('UTC time:', dt.toISOString())

// Add 5.5 hours
const istTime = new Date(dt.getTime() + (5.5 * 60 * 60 * 1000))
console.log('IST time object:', istTime)
console.log('IST UTC time:', istTime.toISOString())

console.log('getUTCHours():', istTime.getUTCHours())
console.log('getHours():', istTime.getHours())

// Expected: 02:40:21 UTC + 5:30 = 08:10:21 IST
console.log('Expected: 08:10:21 AM')
console.log('Actual UTC hours:', istTime.getUTCHours())
console.log('Actual local hours:', istTime.getHours())
