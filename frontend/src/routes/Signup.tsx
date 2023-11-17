
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function Signup() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-800">
      <div className="w-full max-w-md mx-auto p-6 space-y-6 border rounded-lg shadow-lg bg-white dark:bg-gray-900">
        <h1 className="text-3xl font-bold text-center">Signup</h1>
        <form className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input
              className="w-full px-3 py-2 border rounded-lg"
              id="username"
              placeholder="Enter your username"
              required
              type="text"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              className="w-full px-3 py-2 border rounded-lg"
              id="password"
              placeholder="Enter your password"
              required
              type="password"
            />
          </div>
          <div>
            <Button
              className="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded-lg hover:bg-blue-700"
              type="submit"
            >
              Create Account
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

