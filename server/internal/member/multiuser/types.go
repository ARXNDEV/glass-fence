package multiuser

import "github.com/ARXNDEV/glass-fence/server/pkg/types"

type Config struct {
	AdminPassword string
	UserPassword  string
	AdminProfile  types.MemberProfile
	UserProfile   types.MemberProfile
}
